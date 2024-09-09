import numpy as np
import pandas as pd

class ValidationUtils:
    def __init__(self, meta_pred_true):
        if type(meta_pred_true) == dict:
            self.meta_pred_true = pd.DataFrame(meta_pred_true).T
        else:
            self.meta_pred_true = meta_pred_true

    def filter_attribute_by_dict(self, target_attribute_dict=None):
        """
        Filters data by more than one attribute.
        """
        if bool(target_attribute_dict) != False:
            all_params = target_attribute_dict.keys()
            filtered_meta_pred_true = self.meta_pred_true.copy()
            for target_attribute in all_params:
                if self.is_list_numeric(self.meta_pred_true[target_attribute].values):
                    slider_min, slider_max = target_attribute_dict[target_attribute]
                    filtered_meta_pred_true = filtered_meta_pred_true[
                        self.meta_pred_true[target_attribute].between(
                            slider_min, slider_max
                        )
                    ]
                else:
                    target_value = target_attribute_dict[target_attribute]
                    filtered_meta_pred_true = filtered_meta_pred_true[
                        self.meta_pred_true[target_attribute] == target_value
                    ]
            return filtered_meta_pred_true
        else:
            return self.meta_pred_true

    @staticmethod
    def filter_validation_collection_by_meta(validation_collection_data, meta_filter):
        filtered_validation_collection_data = []
        allowed_meta_keys = list(meta_filter.keys())
        for doc in validation_collection_data:
            add = ValidationUtils.is_meta_in_range(
                meta_data=doc.meta_data, meta_filter=meta_filter
            )
            if add:
                for meta_name in list(
                    set(doc.meta_data.keys()) - set(allowed_meta_keys)
                ):
                    doc.meta_data.pop(meta_name)
                filtered_validation_collection_data.append(doc.dict())
        return filtered_validation_collection_data

    @staticmethod
    def is_meta_in_range(meta_data, meta_filter):
        """
        Returns boolean value if given the meta value(meta filter) is in the meta data.
        """
        add = True
        for meta_key in meta_filter:
            if type(meta_filter[meta_key]) == str:
                if meta_data[meta_key] != meta_filter[meta_key]:
                    add = False
            elif type(meta_filter[meta_key]) == list:
                if meta_filter[meta_key][0] == "str":
                    for meta_key in meta_filter:
                        add_multi = []
                        if type(meta_filter[meta_key]) == str:
                            if meta_data[meta_key] != meta_filter[meta_key]:
                                add_multi.append(False)
                    add = any(add_multi)
                elif (
                    not min(meta_filter[meta_key])
                    <= meta_data[meta_key]
                    <= max(meta_filter[meta_key])
                ):
                    add = False
        return add

    def filter_attribute(self, target_attribute_dict):
        """
        Filters data by single attribute.
        """
        target_attribute = list(target_attribute_dict.keys())[0]
        target_value = target_attribute_dict[target_attribute]
        if self.is_list_numeric(self.meta_pred_true[target_attribute].values):
            slider_min, slider_max = target_attribute_dict[target_attribute]
            filtered_meta_pred_true = self.meta_pred_true[
                self.meta_pred_true[target_attribute].between(slider_min, slider_max)
            ]
        else:
            filtered_meta_pred_true = self.meta_pred_true[
                self.meta_pred_true[target_attribute] == target_value
            ]
        return filtered_meta_pred_true

    def multifilter_attribute(self, target_attributes_dict):
        """
        Filters data by more than one attribute.
        """
        all_params = target_attributes_dict.keys()
        filtered_meta_pred_true = self.meta_pred_true.copy()
        for target_attribute in all_params:
            if self.is_list_numeric(self.meta_pred_true[target_attribute].values):
                slider_min, slider_max = target_attributes_dict[target_attribute]
                filtered_meta_pred_true = filtered_meta_pred_true[
                    self.meta_pred_true[target_attribute].between(
                        slider_min, slider_max
                    )
                ]
            else:
                target_value = target_attributes_dict[target_attribute]
                filtered_meta_pred_true = filtered_meta_pred_true[
                    self.meta_pred_true[target_attribute] == target_value
                ]
        return filtered_meta_pred_true

    # Typecheckers
    @staticmethod
    def is_list_numeric(x_list):
        return all(
            [
                isinstance(
                    i,
                    (
                        int,
                        float,
                        np.int,
                        np.int8,
                        np.int16,
                        np.int32,
                        np.float,
                        np.float16,
                        np.float32,
                        np.float64,
                    ),
                )
                for i in x_list
            ]
        )

    @staticmethod
    def polygon_to_mask(poly, shape, max_value=1):
        import skimage

        if type(shape) == int:
            img = np.zeros((shape, shape, 1), "uint8")
        else:
            shape = int(shape[0]), int(shape[1]), 1
            img = np.zeros(shape)
        xs = [xy["x"] for xy in poly]
        ys = [xy["y"] for xy in poly]
        # fill polygon

        rr, cc = skimage.draw.polygon(xs, ys, img.shape)
        img[rr, cc] = max_value
        return img

    @staticmethod
    def rle_to_mask(mask_rle: str, shape, label=1):
        """
        mask_rle: run-length as string formatted (start length)
        shape: (height,width) of array to return
        Returns numpy array, 1 - mask, 0 - background

        """
        s = mask_rle.split()
        starts, lengths = [np.asarray(x, dtype=int) for x in (s[0:][::2], s[1:][::2])]
        starts -= 1
        ends = starts + lengths
        img = np.zeros(shape[0] * shape[1], dtype=np.uint8)
        for lo, hi in zip(starts, ends):
            img[lo:hi] = label
        return img.reshape(shape)  # Needed to align to RLE direction

    @staticmethod
    def mask_to_rle(image):
        """
        img: numpy array, 1 - mask, 0 - background
        Returns run length as string formatted
        Assumas image shape is (n,n) or (n,n,1)
        """
        image_shape = image.shape
        pixels = image.flatten()
        pixels = np.concatenate([[0], pixels, [0]])
        runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
        runs[1::2] -= runs[::2]
        rle_string = " ".join(str(x) for x in runs)

        return rle_string, image_shape

    @staticmethod
    def polygon_to_rle(polygon: list, shape):
        import cv2
        from pycocotools.mask import encode
        
        mask = np.zeros(shape, dtype=np.uint8)
        polygon = np.asarray(polygon)
        polygon = polygon.reshape(-1, 2)
        cv2.fillPoly(mask, [polygon], 1)

        rle = encode(np.asfortranarray(mask))  # Encoding the mask into RLE
        rle["counts"] = rle["counts"].decode("utf-8")
        return rle

    @staticmethod
    def calculate_iou(gt_mask, pred_mask, threshold=0.5):
        """
        Calculate the Intersection over Union (IoU) of two bounding boxes.

        Parameters
        ----------
        gt_box : dict
            Keys: {'x1', 'x2', 'y1', 'y2'}
            The (x1, y1) position is at the top left corner,
            the (x2, y2) position is at the bottom right corner
        pred_box : dict
            Keys: {'x1', 'x2', 'y1', 'y2'}
            The (x, y) position is at the top left corner,
            the (x2, y2) position is at the bottom right corner

        Returns
        -------
        float
            in [0, 1]
        """
        # Don't even convert polygons to mask if there's no intersection
        gt_xs, gt_ys = [i["x"] for i in gt_mask], [i["y"] for i in gt_mask]
        min_gt_x, max_gt_x = min(gt_xs), max(gt_xs)
        min_gt_y, max_gt_y = min(gt_ys), max(gt_ys)

        pred_xs, pred_ys = [i["x"] for i in pred_mask], [i["y"] for i in pred_mask]
        min_pred_x, max_pred_x = min(pred_xs), max(pred_xs)
        min_pred_y, max_pred_y = min(pred_ys), max(pred_ys)

        shape = max(max_pred_x, max_gt_x, max_gt_y, max_pred_y)

        is_intersect = (max(min_gt_x, min_pred_x) < min(max_gt_x, max_pred_x)) and (
            max(min_gt_y, min_pred_y) < min(max_gt_y, max_pred_y)
        )
        if not is_intersect:
            iou = 0
            return iou

        mask1 = ValidationUtils.polygon_to_mask(gt_mask, shape=shape)
        mask2 = ValidationUtils.polygon_to_mask(pred_mask, shape=shape)

        mask1_area = np.count_nonzero(mask1 == 1)
        mask2_area = np.count_nonzero(mask2 == 1)
        intersection = np.count_nonzero(np.logical_and(mask1 == 1, mask2 == 1))
        iou = intersection / (mask1_area + mask2_area - intersection)
        return iou


class Statistics:
    @staticmethod
    def calculate_confidence_interval(metric, len_, z_value=1.96):
        metric = np.abs(metric)
        ci_length = z_value * np.sqrt((metric * (1 - metric)) / len_)
        ci_lower = metric - ci_length
        ci_upper = metric + ci_length
        return (ci_lower, ci_upper)

    @staticmethod
    def calculate_histogram(array_, min_, max_, n_bins):
        array = np.array(array_)
        bin_spaces = np.linspace(min_, max_, n_bins + 1)
        histogram_list = list()

        for i in range(len(bin_spaces) - 1):
            bin_min = bin_spaces[i]
            bin_max = bin_spaces[i + 1]
            histogram_list.append(
                {
                    "category": f"{bin_min.round(2)}",
                    "value": np.sum([(bin_min < array_) & (array_ <= bin_max)]).item(),
                }
            )

        return histogram_list