from ebx.models.exec_parameters import Config


def test_can_load_exec_parameters():
    data = {
        'max_pixels': 1000,
        'scale': 2,
        'best_effort': True
    }
    config = Config(**data)
    assert config.max_pixels == data['max_pixels']
    assert config.scale == data['scale']
    assert config.best_effort == data['best_effort']