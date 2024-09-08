.. SPDX-FileCopyrightText: Copyright © 2023 Idiap Research Institute <contact@idiap.ch>
..
.. SPDX-License-Identifier: GPL-3.0-or-later

.. _mednet:

==============================================================================
 Multi-task Library to Develop Computer-Aided Tools for Medical Data Analysis
==============================================================================

.. todolist::

Framework for development and analysis of deep neural network architectures
applied to medical data (images, 2D and 3D). This package can be readily used
on a number of public datasets.  It can be extended to add more datasets, and
models.

Use one or more the BibTeX references below to cite this work:

.. code:: bibtex

   @INPROCEEDINGS{raposo_union_2022,
      author = {Raposo, Geoffrey and Trajman, Anete and Anjos, Andr{\'{e}}},
      month = 11,
      title = {Pulmonary Tuberculosis Screening from Radiological Signs on Chest X-Ray Images Using Deep Models},
      booktitle = {Union World Conference on Lung Health},
      year = {2022},
      date = {2022-11-01},
      organization = {The Union},
   }

   @TECHREPORT{Raposo_Idiap-Com-01-2021,
      author = {Raposo, Geoffrey},
      keywords = {deep learning, generalization, Interpretability, transfer learning, Tuberculosis Detection},
      projects = {Idiap},
      month = {7},
      title = {Active tuberculosis detection from frontal chest X-ray images},
      type = {Idiap-Com},
      number = {Idiap-Com-01-2021},
      year = {2021},
      institution = {Idiap},
      url = {https://gitlab.idiap.ch/biosignal/software/mednet},
      pdf = {https://publidiap.idiap.ch/downloads/reports/2021/Raposo_Idiap-Com-01-2021.pdf}
   }

   @INPROCEEDINGS{renzo_2021,
       title     = {Development of a lung segmentation algorithm for analog imaged chest X-Ray: preliminary results},
       author    = {Matheus A. Renzo and Nat\'{a}lia Fernandez and Andr\'e Baceti and Natanael Nunes de Moura Junior and Andr\'e Anjos},
       month     = {10},
       booktitle = {XV Brazilian Congress on Computational Intelligence},
       year      = {2021},
       url       = {https://publications.idiap.ch/index.php/publications/show/4649},
   }

   @MISC{laibacher_2019,
       title         = {On the Evaluation and Real-World Usage Scenarios of Deep Vessel Segmentation for Retinography},
       author        = {Tim Laibacher and Andr\'e Anjos},
       year          = {2019},
       eprint        = {1909.03856},
       archivePrefix = {arXiv},
       primaryClass  = {cs.CV},
       url           = {https://arxiv.org/abs/1909.03856},
   }


User Guide
----------

.. toctree::
   :maxdepth: 2

   install
   usage/index
   baselines
   data-model
   databases/index
   models
   references
   cli
   api
   config
   contribute


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. include:: links.rst
