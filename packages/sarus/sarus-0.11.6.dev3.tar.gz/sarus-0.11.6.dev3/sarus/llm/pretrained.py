import enum
from typing import Literal, Optional, Union, cast

import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.dataset import make_prompts
from sarus_data_spec.scalar import pretrained_model
from sarus_data_spec.transform import fit_model, generate_from_model

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.pandas.dataframe import DataFrame
from sarus.utils import register_ops


class TrainState: ...


class SampleType(str, enum.Enum):
    PRETRAIN = "pretrain"
    INSTRUCT = "instruct"


class LLM(DataSpecWrapper[TrainState]):
    def __init__(self, name: str, sample_type: SampleType) -> None:
        self.name = name
        if name not in [
            "llama3-8b",
            "open_mistral_7b",
            "llama3-70b",
            "phi_3_mini",
        ]:
            raise ValueError("Unknown model name.")
        model_dataspec = pretrained_model(self.name, sample_type)
        self._set_dataspec(model_dataspec)

    def fit(
        self,
        X: DataSpecWrapper,
        batch_size: int,
        text_field: Optional[str] = None,
        answer_field: Optional[str] = None,
        question_field: Optional[str] = None,
        epochs: int = -1,
        X_val: Optional[DataSpecWrapper] = None,
    ) -> None:
        if not isinstance(X, DataSpecWrapper):
            raise TypeError(
                f"Cannot fit {self.name} on `X` because it is not a Sarus object."
            )

        input_ds = X.dataspec()
        if input_ds.prototype() != sp.Dataset:
            raise TypeError(
                f"Cannot fit {self.name} on `X` because it is not a Sarus Dataset."
            )
        model_ds = self.dataspec()
        if X_val is not None:
            if not isinstance(X_val, DataSpecWrapper):
                raise TypeError("X_val should be a DataSpecWrapper.")
            val_ds = X_val.dataspec()
            fitted_dataspec = fit_model(
                epochs=epochs,
                batch_size=batch_size,
                text_field=text_field,
                question_field=question_field,
                answer_field=answer_field,
            )(model=model_ds, dataset=input_ds, validation_dataset=val_ds)
        else:
            fitted_dataspec = fit_model(
                epochs=epochs,
                batch_size=batch_size,
                text_field=text_field,
                question_field=question_field,
                answer_field=answer_field,
            )(model=model_ds, dataset=input_ds)

        self._set_dataspec(fitted_dataspec)
        return self

    def sample(
        self,
        prompts,
        temperature: float = 1.0,
        max_new_tokens: int = 20,
    ):
        if not isinstance(prompts, st.DataSpec):
            prompts = make_prompts(prompts)
        samples = generate_from_model(
            temperature=temperature, max_new_tokens=max_new_tokens
        )(model=self.dataspec(), prompts=prompts)

        return DataFrame.from_dataspec(samples)

    def __sarus_eval__(
        self,
        target_epsilon: Union[Optional[float], Literal["unlimited"]] = None,
        verbose: Optional[int] = None,
    ) -> str:
        _ = super().__sarus_eval__(target_epsilon, verbose)

        scalar = cast(st.Scalar, self.dataspec())
        if scalar.is_pretrained_model():
            return "model (pretrained)"
        elif scalar.is_fitted_model():
            return "model (fitted)"
        else:
            raise TypeError(
                "The wrapped scalar is not a pretrained or a fitted model."
            )


register_ops()
