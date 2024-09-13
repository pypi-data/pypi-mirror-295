# pyright: reportAttributeAccessIssue=false

from collections.abc import Iterable
from typing import TypeVar

import torch
import torcheval.metrics


TAmexMetric = TypeVar("TAmexMetric", bound="AmexMetric")
TNegMeanSquaredError = TypeVar("TNegMeanSquaredError")
TPrimeNetAccuracy = TypeVar("TPrimeNetAccuracy", bound="PrimeNetAccuracy")


class AmexMetric(torcheval.metrics.Metric):
    def __init__(self, *_, **__):
        super().__init__()
        self._add_state("preds", [])
        self._add_state("gts", [])

    @torch.inference_mode()
    def update(self, pred: torch.Tensor, gt: torch.Tensor):  # pyright: ignore
        self.preds.append(pred)
        self.gts.append(gt)
        return self

    @torch.inference_mode()
    def merge_state(self, metrics: Iterable[TAmexMetric]):  # pyright: ignore
        for metric in metrics:
            self.preds.extend(metric.preds)
            self.gts.extend(metric.gts)
        return self

    @torch.inference_mode()
    def compute(self):
        preds = torch.cat(self.preds)
        gts = torch.cat(self.gts)
        assert preds.device == gts.device
        # count of positives and negatives
        n_pos = gts.sum()
        n_neg = len(gts) - n_pos

        # sorting by descring prediction values
        indices = torch.argsort(preds[:, 1], descending=True)
        target = gts[indices]

        # filter the top 4% by cumulative row weights
        weight = 20.0 - target * 19.0
        cum_norm_weight = (weight / weight.sum()).cumsum(dim=0)
        four_pct_filter = cum_norm_weight <= 0.04

        # default rate captured at 4%
        d = target[four_pct_filter].sum() / n_pos

        # weighted gini coefficient
        lorentz = (target / n_pos).cumsum(dim=0)
        gini = ((lorentz - cum_norm_weight) * weight).sum()

        # max weighted gini coefficient
        gini_max = 10 * n_neg * (1 - 19 / (n_pos + 20 * n_neg))

        # normalized weighted gini coefficient
        g = gini / gini_max

        return 0.5 * (g + d)


class PrimeNetAccuracy(torcheval.metrics.Metric):
    def __init__(self, *_, **__):
        super().__init__()
        self._add_state("correct", 0)
        self._add_state("total", 0)

    @torch.inference_mode()
    def update(self, pred: torch.Tensor, _):  # pyright: ignore
        self.correct += pred.correct_num
        self.total += pred.total_num
        return self

    @torch.inference_mode()
    def merge_state(self, metrics: Iterable[TPrimeNetAccuracy]):  # pyright: ignore
        for metric in metrics:
            self.correct += metric.correct
            self.total += metric.total
        return self

    @torch.inference_mode()
    def compute(self):
        return torch.tensor([self.correct / self.total])


class NegRootMeanSquaredError(torcheval.metrics.MeanSquaredError):
    @torch.inference_mode()
    def update(self, pred, target):  # pyright: ignore
        if pred.device != target.device:
            target = target.to(pred.device)
        self = super().update(pred, target)
        return self

    @torch.inference_mode()
    def compute(self: TNegMeanSquaredError) -> torch.Tensor:  # pyright: ignore
        return -1 * torch.sqrt(super().compute())


class LoggingMetric(torcheval.metrics.Metric):
    def __init__(self, key, *_, **__):
        super().__init__()
        self.key = key
        self._add_state("sum", 0)
        self._add_state("total", 0)

    @torch.inference_mode()
    def update(self, pred: torch.Tensor, _):  # pyright: ignore
        self.sum += (
            pred[self.key].item()
            if isinstance(pred[self.key], torch.Tensor)
            else pred[self.key]
        )
        self.total += 1
        return self

    @torch.inference_mode()
    def merge_state(self, metrics):  # pyright: ignore
        for metric in metrics:
            self.sum += metric.sum
            self.total += metric.total
        return self

    @torch.inference_mode()
    def compute(self):
        return torch.tensor([self.sum / self.total])


class MLEM_total_mse_loss(LoggingMetric):  # noqa: N801
    def __init__(self, *_, **__):
        super().__init__("total_mse_loss")


class MLEM_total_CE_loss(LoggingMetric):  # noqa: N801
    def __init__(self, *_, **__):
        super().__init__("total_CE_loss")


class MLEM_sparcity_loss(LoggingMetric):  # noqa: N801
    def __init__(self, *_, **__):
        super().__init__("sparcity_loss")


class MLEM_reconstruction_loss(LoggingMetric):  # noqa: N801
    def __init__(self, *_, **__):
        super().__init__("reconstruction_loss")
