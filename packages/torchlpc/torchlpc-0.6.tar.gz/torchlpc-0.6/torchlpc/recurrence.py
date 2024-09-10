import torch
import torch.nn.functional as F
from torch.autograd import Function
from numba import cuda
from typing import Tuple, Optional, Any, List

from .parallel_scan import compute_linear_recurrence


class RecurrenceCUDA(Function):
    @staticmethod
    def forward(
        decay: torch.Tensor,
        impulse: torch.Tensor,
        initial_state: torch.Tensor,
    ) -> torch.Tensor:
        n_dims, n_steps = decay.shape
        out = torch.empty_like(impulse)
        compute_linear_recurrence(
            cuda.as_cuda_array(decay.detach()),
            cuda.as_cuda_array(impulse.detach()),
            cuda.as_cuda_array(initial_state.detach()),
            cuda.as_cuda_array(out),
            n_dims,
            n_steps,
        )
        return out

    @staticmethod
    def setup_context(ctx: Any, inputs: List[Any], output: Any) -> Any:
        decay, _, initial_state = inputs
        ctx.save_for_backward(decay, initial_state, output)
        ctx.save_for_forward(decay, initial_state, output)

    @staticmethod
    def backward(
        ctx: Any, grad_out: torch.Tensor
    ) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor], Optional[torch.Tensor]]:
        decay, initial_state, out = ctx.saved_tensors
        grad_decay = grad_impulse = grad_initial_state = None
        n_dims, _ = decay.shape

        padded_decay = F.pad(decay.unsqueeze(1), (0, 1)).squeeze(1)
        if ctx.needs_input_grad[2]:
            padded_grad_out = F.pad(grad_out.unsqueeze(1), (1, 0)).squeeze(1)
        else:
            padded_grad_out = grad_out
            padded_decay = padded_decay[:, 1:]

        init = padded_grad_out.new_zeros(n_dims)
        flipped_grad_impulse = RecurrenceCUDA.apply(
            padded_decay.flip(1).conj_physical(),
            padded_grad_out.flip(1),
            init,
        )

        if ctx.needs_input_grad[2]:
            grad_initial_state = flipped_grad_impulse[:, -1]
            flipped_grad_impulse = flipped_grad_impulse[:, :-1]

        if ctx.needs_input_grad[1]:
            grad_impulse = flipped_grad_impulse.flip(1)

        if ctx.needs_input_grad[0]:
            valid_out = out[:, :-1]
            padded_out = torch.cat([initial_state.unsqueeze(1), valid_out], dim=1)
            grad_decay = padded_out.conj_physical() * flipped_grad_impulse.flip(1)

        return grad_decay, grad_impulse, grad_initial_state

    @staticmethod
    def jvp(
        ctx: Any,
        grad_decay: torch.Tensor,
        grad_impulse: torch.Tensor,
        grad_initial_state: torch.Tensor,
    ) -> torch.Tensor:
        decay, initial_state, out = ctx.saved_tensors

        fwd_initial_state = (
            grad_initial_state
            if grad_initial_state is not None
            else torch.zeros_like(initial_state)
        )
        fwd_impulse = (
            grad_impulse if grad_impulse is not None else torch.zeros_like(out)
        )

        if grad_decay is not None:
            concat_out = torch.cat([initial_state.unsqueeze(1), out[:, :-1]], dim=1)
            fwd_decay = concat_out * grad_decay
            fwd_impulse = fwd_impulse + fwd_decay

        return RecurrenceCUDA.apply(decay, fwd_impulse, fwd_initial_state)

    @staticmethod
    def vmap(info, in_dims, *args):
        def maybe_expand_bdim_at_front(x, x_bdim):
            if x_bdim is None:
                return x.expand(info.batch_size, *x.shape)
            return x.movedim(x_bdim, 0)

        decay, impulse, initial_state = tuple(
            map(
                lambda x: x.reshape(-1, *x.shape[2:]),
                map(maybe_expand_bdim_at_front, args, in_dims),
            )
        )

        out = RecurrenceCUDA.apply(decay, impulse, initial_state)
        return out.reshape(info.batch_size, -1, *out.shape[1:]), 0
