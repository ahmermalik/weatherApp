import models


def forward():
    models.DB.create_tables([models.weather_table])


if __name__ == '__main__':
    forward()