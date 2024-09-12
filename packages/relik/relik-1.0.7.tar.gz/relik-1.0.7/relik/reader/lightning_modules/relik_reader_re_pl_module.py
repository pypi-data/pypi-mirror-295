from typing import Any, Optional

import lightning
from lightning.pytorch.utilities.types import STEP_OUTPUT, OptimizerLRScheduler

from relik.reader.pytorch_modules.triplet import RelikReaderForTripletExtraction


class RelikReaderREPLModule(lightning.LightningModule):
    def __init__(
        self,
        cfg: dict,
        transformer_model: str,
        additional_special_symbols: int,
        additional_special_symbols_types: Optional[int] = 0,
        entity_type_loss: bool = None,
        add_entity_embedding: bool = None,
        num_layers: Optional[int] = None,
        activation: str = "gelu",
        linears_hidden_size: Optional[int] = 512,
        use_last_k_layers: int = 1,
        training: bool = False,
        default_reader_class: str = "relik.reader.pytorch_modules.hf.modeling_relik.RelikReaderREModel",
        *args: Any,
        **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.save_hyperparameters()

        self.relik_reader_re_model = RelikReaderForTripletExtraction(
            transformer_model,
            additional_special_symbols,
            additional_special_symbols_types,
            entity_type_loss,
            add_entity_embedding,
            num_layers,
            activation,
            linears_hidden_size,
            use_last_k_layers,
            training=training,
            default_reader_class=default_reader_class,
            **kwargs,
        )
        self.optimizer_factory = None

    def training_step(self, batch: dict, *args: Any, **kwargs: Any) -> STEP_OUTPUT:
        relik_output = self.relik_reader_re_model(**batch)
        self.log("train-loss", relik_output["loss"])
        self.log("train-start_loss", relik_output["ned_start_loss"])
        self.log("train-end_loss", relik_output["ned_end_loss"])
        self.log("train-relation_loss", relik_output["re_loss"])
        if "ned_type_loss" in relik_output:
            self.log("train-ned_type_loss", relik_output["ned_type_loss"])
        return relik_output["loss"]

    def validation_step(
        self, batch: dict, *args: Any, **kwargs: Any
    ) -> Optional[STEP_OUTPUT]:
        return

    def set_optimizer_factory(self, optimizer_factory) -> None:
        self.optimizer_factory = optimizer_factory

    def configure_optimizers(self) -> OptimizerLRScheduler:
        return self.optimizer_factory(self.relik_reader_re_model)
