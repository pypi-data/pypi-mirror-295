# coding=utf-8
# Copyright 2024 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from tensorflow_datasets.datasets.places365_small import places365_small_dataset_builder
import tensorflow_datasets.testing as tfds_test


class Places365SmallTest(tfds_test.DatasetBuilderTestCase):
  DATASET_CLASS = places365_small_dataset_builder.Builder
  SPLITS = {'train': 2, 'test': 2, 'validation': 2}

  DL_DOWNLOAD_RESULT = {
      'train': 'data_256.tar',
      'test': 'test_256.tar',
      'validation': 'val_256.tar',
  }
  DL_EXTRACT_RESULT = 'annotation'


if __name__ == '__main__':
  tfds_test.test_main()
