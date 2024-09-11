"""
********************************************************************************
aixd.mlmodel
********************************************************************************

This package contains the machine-learning model implementation.

.. currentmodule:: aixd.mlmodel.data

Data Loading
------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~data_loader.DataModule


.. currentmodule:: aixd.mlmodel.architecture

Architecture
------------

Models
~~~~~~

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~cond_ae_model.CondAEModel
    ~cond_vae_model.CondVAEModel
    ~two_stage_model.InverseModel
    ~two_stage_model.FreezeEncoder

Blocks
~~~~~~

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~blocks.ResBlockFC
    ~blocks.ResBlockConv
    ~blocks.ResBlock1D
    ~blocks.ResBlock2D
    ~blocks.ResBlock3D
    ~blocks.SelfAttn
    ~blocks.SelfAttn1D
    ~blocks.SelfAttn2D
    ~blocks.SelfAttn3D
    ~blocks.Activation

Decoders/Encoders
~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~decoders.Decoder
    ~encoders.Encoder
    ~encoders.VEncoder

Heads
~~~~~

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~heads.InHeadFC
    ~heads.OutHeadFC
    ~heads.InHeadConv
    ~heads.OutHeadConv
    ~heads.InHeadConv1D
    ~heads.OutHeadConv1D
    ~heads.InHeadConv2D
    ~heads.OutHeadConv2D
    ~heads.InHeadConv3D
    ~heads.OutHeadConv3D

Losses
~~~~~~

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~losses.LossStd
    ~losses.MGEloss


.. currentmodule:: aixd.mlmodel.generation


Generation
----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ~generator.Generator
    ~sampling.GeneratorSampler

"""
