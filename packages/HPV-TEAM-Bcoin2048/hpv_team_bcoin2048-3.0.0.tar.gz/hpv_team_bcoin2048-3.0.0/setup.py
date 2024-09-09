from setuptools import setup, find_packages

setup(
    name='HPV_TEAM_Bcoin2048',                          # Название вашего пакета
    version='3.0.0',                                    # Версия вашего пакета
    author='A_KTO_Tbl',                                 # Автор
    description='Многофункциональный, кроссплатформенный, многопоточный Bcoin2048 AutoBot, с поддержкой прокси и защитой от блокировок',   # Краткое описание
    url='https://t.me/HPV_TEAM',                        # URL проекта (если есть)
    packages=find_packages(),                           # Автоматический поиск пакетов
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.6',                            # Требования к версии Python
    install_requires=[                                  # Зависимости (если есть)
        'colorama',
        'requests==2.31.0',
        'pysocks==1.7.1'
    ]
)
