from __future__ import annotations

import pathlib
import pickle

try:
    import adet
except ImportError:
    raise ImportError(
        "[ERROR] Please install DeepSolo from the following link: https://github.com/rwood-97/DeepSolo"
    )

import numpy as np
import pandas as pd
import torch
from adet.config import get_cfg

try:
    from detectron2.engine import DefaultPredictor
except ImportError:
    raise ImportError("[ERROR] Please install Detectron2")

from adet.utils.vitae_predictor import ViTAEPredictor
from shapely import LineString, MultiPolygon, Polygon

# first assert we are using the deep solo version of adet
if adet.__version__ != "0.2.0-maptextpipeline":
    raise ImportError(
        "[ERROR] Please install MapTextPipeline from the following link: https://github.com/rwood-97/MapTextPipeline"
    )

from .runner_base import Runner


class MapTextRunner(Runner):
    def __init__(
        self,
        patch_df: pd.DataFrame,
        parent_df: pd.DataFrame = None,
        cfg_file: str
        | pathlib.Path = "./MapTextPipeline/configs/ViTAEv2_S/rumsey/final_rumsey.yaml",
        weights_file: str | pathlib.Path = "./rumsey-finetune.pth",
        device: str = "default",
        delimiter: str = ",",
    ) -> None:
        """_summary_

        Parameters
        ----------
        patch_df : pd.DataFrame | str
            The dataframe containing the patch information. If a string, it should be a path to a CSV file.
        parent_df : pd.DataFrame | str, optional
            The dataframe containing the parent information. If a string, it should be a path to a CSV file, by default None.
        cfg_file : str | pathlib.Path, optional
            The path to the config file (yaml), by default "./MapTextPipeline/configs/ViTAEv2_S/rumsey/final_rumsey.yaml"
        weights_file : str | pathlib.Path, optional
            The path to the weights file (.pth), by default, by default "./rumsey-finetune.pth"
        device : str, optional
            The device to use for the model, by default "default". If default, the device will be set to cuda if available, otherwise cpu.
        delimiter : str, optional
            The delimiter to use if loading dataframes from CSV files, by default ",".
        """
        # setup the dataframes
        self._load_df(patch_df, parent_df, delimiter)

        # set up predictions as dictionaries
        self.patch_predictions = {}
        self.parent_predictions = {}
        self.geo_predictions = {}

        # setup the config
        cfg = get_cfg()  # get a fresh new config
        cfg.merge_from_file(cfg_file)
        cfg.MODEL.WEIGHTS = weights_file
        if device == "default":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        cfg.MODEL.DEVICE = device

        self.voc_size = cfg.MODEL.TRANSFORMER.VOC_SIZE
        self.use_customer_dictionary = cfg.MODEL.TRANSFORMER.CUSTOM_DICT
        if self.voc_size == 96:
            self.CTLABELS = [
                " ",
                "!",
                '"',
                "#",
                "$",
                "%",
                "&",
                "'",
                "(",
                ")",
                "*",
                "+",
                ",",
                "-",
                ".",
                "/",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                ":",
                ";",
                "<",
                "=",
                ">",
                "?",
                "@",
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
                "[",
                "\\",
                "]",
                "^",
                "_",
                "`",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
                "{",
                "|",
                "}",
                "~",
            ]
        elif self.voc_size == 37:
            self.CTLABELS = [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
            ]
        elif self.voc_size == 148:
            self.CTLABELS = [
                " ",
                "!",
                '"',
                "#",
                "$",
                "%",
                "&",
                "'",
                "(",
                ")",
                "+",
                ",",
                "-",
                ".",
                "/",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                ":",
                ";",
                "<",
                "=",
                ">",
                "?",
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
                "_",
                "`",
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "m",
                "n",
                "o",
                "p",
                "q",
                "r",
                "s",
                "t",
                "u",
                "v",
                "w",
                "x",
                "y",
                "z",
                "\x8d",
                "\xa0",
                "¡",
                "£",
                "¨",
                "©",
                "®",
                "¯",
                "°",
                "¹",
                "Á",
                "Â",
                "Ã",
                "Ä",
                "Å",
                "É",
                "Ê",
                "Ì",
                "Í",
                "Î",
                "Ó",
                "ß",
                "à",
                "á",
                "â",
                "ä",
                "è",
                "é",
                "ê",
                "ë",
                "í",
                "ï",
                "ñ",
                "ó",
                "ô",
                "õ",
                "ö",
                "ú",
                "û",
                "ü",
                "ÿ",
                "ā",
                "ė",
                "ī",
                "ő",
                "Œ",
                "ŵ",
                "ƙ",
                "ˆ",
                "ˈ",
                "̓",
                "Ї",
                "ї",
                "ḙ",
                "Ṃ",
                "ἀ",
                "‘",
                "’",
                "“",
                "”",
                "‰",
                "›",
            ]
        else:
            with open(self.use_customer_dictionary, "rb") as fp:
                self.CTLABELS = pickle.load(fp)
        # voc_size includes the unknown class, which is not in self.CTABLES
        assert int(self.voc_size - 1) == len(
            self.CTLABELS
        ), f"voc_size is not matched dictionary size, got {int(self.voc_size - 1)} and {len(self.CTLABELS)}."

        # setup the predictor
        if "vitae" in cfg.MODEL.BACKBONE.NAME.lower():
            self.predictor = ViTAEPredictor(cfg)
        self.predictor = DefaultPredictor(cfg)

    def get_patch_predictions(
        self,
        outputs: dict,
        return_dataframe: bool = False,
        min_ioa: float = 0.7,
    ) -> dict | pd.DataFrame:
        """Post process the model outputs to get patch predictions.

        Parameters
        ----------
        outputs : dict
            The outputs from the model.
        return_dataframe : bool, optional
            Whether to return the predictions as a pandas DataFrame, by default False
        min_ioa : float, optional
            The minimum intersection over area to consider two polygons the same, by default 0.7

        Returns
        -------
        dict or pd.DataFrame
            A dictionary containing the patch predictions or a DataFrame if `as_dataframe` is True.
        """
        # key for predictions
        image_id = outputs["image_id"]
        self.patch_predictions[image_id] = []

        # get instances
        instances = outputs["instances"].to("cpu")
        ctrl_pnts = instances.ctrl_points.numpy()
        scores = instances.scores.tolist()
        recs = instances.recs
        bd_pts = np.asarray(instances.bd)

        self._post_process(image_id, ctrl_pnts, scores, recs, bd_pts)
        self._deduplicate(image_id, min_ioa=min_ioa)

        if return_dataframe:
            return self._dict_to_dataframe(self.patch_predictions, geo=False)
        return self.patch_predictions

    def _process_ctrl_pnt(self, pnt):
        points = pnt.reshape(-1, 2)
        return points

    def _ctc_decode_recognition(self, rec):
        last_char = "###"
        s = ""
        for c in rec:
            c = int(c)
            if c < self.voc_size - 1:
                if last_char != c:
                    if (
                        self.voc_size == 37
                        or self.voc_size == 96
                        or self.voc_size == 148
                    ):
                        s += self.CTLABELS[c]
                        last_char = c
                    else:
                        s += str(chr(self.CTLABELS[c]))
                        last_char = c
            else:
                last_char = "###"
        return s

    def _post_process(self, image_id, ctrl_pnts, scores, recs, bd_pnts, alpha=0.4):
        for ctrl_pnt, score, rec, bd in zip(ctrl_pnts, scores, recs, bd_pnts):
            # draw polygons
            if bd is not None:
                bd = np.hsplit(bd, 2)
                bd = np.vstack([bd[0], bd[1][::-1]])
                polygon = Polygon(bd).buffer(0)

                if isinstance(polygon, MultiPolygon):
                    polygon = polygon.convex_hull

            # draw center lines
            line = self._process_ctrl_pnt(ctrl_pnt)
            line = LineString(line)

            # draw text
            text = self._ctc_decode_recognition(rec)
            if self.voc_size == 37:
                text = text.upper()
            # text = "{:.2f}: {}".format(score, text)
            text = f"{text}"
            score = f"{score:.2f}"

            self.patch_predictions[image_id].append([polygon, text, score])

    @staticmethod
    def _dict_to_dataframe(
        preds: dict,
        geo: bool = False,
        parent: bool = False,
    ) -> pd.DataFrame:
        """Convert the predictions dictionary to a pandas DataFrame.

        Parameters
        ----------
        preds : dict
            A dictionary of predictions.
        geo : bool, optional
            Whether the dictionary is georeferenced coords (or pixel bounds), by default True
        parent : bool, optional
            Whether the dictionary is at parent level, by default False

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the predictions.
        """
        if geo:
            columns = ["polygon", "crs", "text", "score"]
        else:
            columns = ["polygon", "text", "score"]

        if parent:
            columns.append("patch_id")

        preds_df = pd.concat(
            pd.DataFrame(
                preds[k],
                index=np.full(len(preds[k]), k),
                columns=columns,
            )
            for k in preds.keys()
        )
        preds_df.index.name = "image_id"
        preds_df.reset_index(inplace=True)  # reset index to get image_id as a column
        return preds_df
