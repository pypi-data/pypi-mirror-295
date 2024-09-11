import torch


class CDistLoss(torch.nn.Module):
    def __init__(self, p=1., hardness_ratio=.1, cast_to_double=False, margin=0.0) -> None:
        super().__init__()
        self.p = p
        self.hardness_ratio = hardness_ratio
        self.cast_to_double = cast_to_double
        self.margin = margin

    def forward(self, x, y):
        assert x.size(0) == y.size(0)
        assert x.dim() == 2
        assert y.dim() == 1
        assert y.dtype == torch.int64 or y.dtype == torch.bool

        # TODO(anguelos) Verify this is the apropriate way to avoid a loss that is detached from the features
        if y.float().std() == 0:
            return .00000001 * torch.sum(x, dim=1)

        if self.cast_to_double:
            x = x.double()

        D = torch.cdist(x, x, p=self.p)

        with torch.no_grad():
            agree = (y[None, :] == y[:, None]).float()
            disagree = 1 - agree
            valid_rows = (agree.sum(dim=1) > 1) & (disagree.sum(dim=1) > 0)
            agree = agree[valid_rows, :]
            disagree = disagree[valid_rows, :]

        D = D[valid_rows, :]

        if D.size(0) == 0:
            return torch.tensor(0.0, device=D.device)

        with torch.no_grad():
            col_idx = torch.argsort(D, dim=1)
            col_idx = col_idx[:, 1:]  # Remove self match
            row_idx = torch.arange(D.size(0), dtype=torch.int64)[:, None].expand_as(col_idx)
            agree = agree[row_idx, col_idx]
            disagree = disagree[row_idx, col_idx]
            #valid_rows = (agree.sum(dim=1) > 0) & (disagree.sum(dim=1) > 0)

        dist = D[row_idx, col_idx]

        with torch.no_grad():
            found_agree = agree.cumsum(dim=1)
            found_agree /= (found_agree.sum(dim=1)[:, None] + .0000001)
            found_disagree = disagree.cumsum(dim=1)
            found_disagree /= (found_disagree.sum(dim=1)[:, None] + .0000001)
            negative_hardness = disagree * (found_disagree / (found_agree + self.hardness_ratio))
            positive_hardness = agree * ((found_disagree + self.hardness_ratio) / (found_agree + self.hardness_ratio))

        per_sample_score = torch.relu(dist * positive_hardness + self.margin - dist * negative_hardness).mean(dim=1)

        with torch.no_grad():
            sample_performance = (found_agree - found_disagree).sum(dim=1)
            sample_performance -= sample_performance.min()
            sample_weight = 1 / (sample_performance + 1)  # TODO(anguelos) test sample_weight = sample_performance + 1

        return (per_sample_score * sample_weight)


class CDistRatioLoss(torch.nn.Module):
    def __init__(self, p=1., hardness_ratio=.1, cast_to_double=False, margin=0.0) -> None:
        super().__init__()
        self.p = p
        self.hardness_ratio = hardness_ratio
        self.cast_to_double = cast_to_double
        self.margin = margin

    def forward(self, x, y):
        assert x.size(0) == y.size(0)
        assert x.dim() == 2
        assert y.dim() == 1
        assert y.dtype == torch.int64 or y.dtype == torch.bool

        # TODO(anguelos) Verify this is the apropriate way to avoid a loss that is detached from the features
        if y.float().std() == 0:
            return .00000001 * torch.sum(x, dim=1)

        if self.cast_to_double:
            x = x.double()

        D = torch.cdist(x, x, p=self.p)

        with torch.no_grad():
            agree = (y[None, :] == y[:, None]).float()
            disagree = 1 - agree
            valid_rows = (agree.sum(dim=1) > 1) & (disagree.sum(dim=1) > 0)
            agree = agree[valid_rows, :]
            disagree = disagree[valid_rows, :]

        D = D[valid_rows, :]

        if D.size(0) == 0:
            return torch.tensor(0.0, device=D.device)

        with torch.no_grad():
            col_idx = torch.argsort(D, dim=1)
            col_idx = col_idx[:, 1:]  # Remove self match
            row_idx = torch.arange(D.size(0), dtype=torch.int64)[:, None].expand_as(col_idx)
            agree = agree[row_idx, col_idx]
            disagree = disagree[row_idx, col_idx]

        dist = D[row_idx, col_idx]

        with torch.no_grad():
            agree_count = agree.sum(dim=1, keepdim=True)
            found_disagree = disagree.cumsum(dim=1)
            hardest_negatives = (found_disagree <= agree_count).float() * disagree

        d_p = (dist * agree).sum(dim=1)
        d_n = (dist * hardest_negatives).sum(dim=1)
        return (d_p / (d_p + d_n + .0001)) ** 2


class CDistTripletLoss(torch.nn.Module):
    def __init__(self, p=1., hardness_ratio=.1, cast_to_double=False, margin=0.0) -> None:
        super().__init__()
        self.p = p
        self.hardness_ratio = hardness_ratio
        self.cast_to_double = cast_to_double
        self.margin = margin

    def forward(self, x, y):
        assert x.size(0) == y.size(0)
        assert x.dim() == 2
        assert y.dim() == 1
        assert y.dtype == torch.int64 or y.dtype == torch.bool

        # TODO(anguelos) Verify this is the apropriate way to avoid a loss that is detached from the features
        if y.float().std() == 0:
            return .00000001 * torch.sum(x, dim=1)

        if self.cast_to_double:
            x = x.double()

        D = torch.cdist(x, x, p=self.p)

        with torch.no_grad():
            agree = (y[None, :] == y[:, None]).float()
            disagree = 1 - agree
            valid_rows = (agree.sum(dim=1) > 1) & (disagree.sum(dim=1) > 0)
            agree = agree[valid_rows, :]
            disagree = disagree[valid_rows, :]

        D = D[valid_rows, :]

        if D.size(0) == 0:
            return torch.tensor(0.0, device=D.device)

        with torch.no_grad():
            col_idx = torch.argsort(D, dim=1)
            col_idx = col_idx[:, 1:]  # Remove self match
            row_idx = torch.arange(D.size(0), dtype=torch.int64)[:, None].expand_as(col_idx)
            agree = agree[row_idx, col_idx]
            disagree = disagree[row_idx, col_idx]

        dist = D[row_idx, col_idx]

        with torch.no_grad():
            agree_count = agree.sum(dim=1, keepdim=True)
            found_disagree = disagree.cumsum(dim=1)
            hardest_negatives = (found_disagree <= agree_count).float() * disagree

        Dw_ap = (dist * agree).sum(dim=1)
        Dw_an = (dist * hardest_negatives).sum(dim=1)
        return torch.relu(Dw_ap - Dw_an + self.margin)


class CDistContrastiveLoss(torch.nn.Module):
    def __init__(self, p=1., hardness_ratio=.1, cast_to_double=False, margin=0.0) -> None:
        super().__init__()
        self.p = p
        self.hardness_ratio = hardness_ratio
        self.cast_to_double = cast_to_double
        self.margin = margin

    def forward(self, x, y):
        assert x.size(0) == y.size(0)
        assert x.dim() == 2
        assert y.dim() == 1
        assert y.dtype == torch.int64 or y.dtype == torch.bool

        # TODO(anguelos) Verify this is the apropriate way to avoid a loss that is detached from the features
        if y.float().std() == 0:
            return .00000001 * torch.sum(x, dim=1)

        if self.cast_to_double:
            x = x.double()

        D = torch.cdist(x, x, p=self.p)

        with torch.no_grad():
            agree = (y[None, :] == y[:, None]).float()
            disagree = 1 - agree
            valid_rows = (agree.sum(dim=1) > 1) & (disagree.sum(dim=1) > 0)
            agree = agree[valid_rows, :]
            disagree = disagree[valid_rows, :]

        D = D[valid_rows, :]

        if D.size(0) == 0:
            return torch.tensor(0.0, device=D.device)

        with torch.no_grad():
            col_idx = torch.argsort(D, dim=1)
            col_idx = col_idx[:, 1:]  # Remove self match
            row_idx = torch.arange(D.size(0), dtype=torch.int64)[:, None].expand_as(col_idx)
            agree = agree[row_idx, col_idx]
            disagree = disagree[row_idx, col_idx]

        dist = D[row_idx, col_idx]

        with torch.no_grad():
            agree_count = agree.sum(dim=1, keepdim=True)
            found_disagree = disagree.cumsum(dim=1)
            hardest_negatives = (found_disagree <= agree_count).float() * disagree

        return .5 * agree * dist + hardest_negatives * torch.relu(self.margin - dist)
