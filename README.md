<p align="center">
    <a href="https://github.com/MODCT/CeleryMath">
        <img src="images/social.png" height="241"/>
    </a>
    <h1 align="center">CeleryMath</h1>
    <p align="center">Another LaTex OCR Project</p>
    <p align="center">Give me a star :star: if you like this project~</p>
    <p align="center"><a href="README.md">English</a> | <a href="README_CN.md">简体中文</a></p>
</p>

![images/cmpreview.gif](https://github.com/MODCT/CeleryMath/blob/main/images/cmpreview.gif)

## Usage

1. Download prebuilt files from [Release](https://github.com/MODCT/CeleryMath/releases).
2. Extract `celeryMah-weights-\*.zip` and `celeryMath-\*.zip`
3. Move `Tokenizer.json`、 `celeryMathEncoder.onnx`、 `celeryMathDecoder.onnx`  to `conf` directory.
4. Open `celeryMath.exe` and Click settings to config path.
5. Have fun!

## Build from source

Install python-poetry first

1. clone repo and creat environment

```console
git clone https://github.com/MODCT/CeleryMath.git
cd CeleryMath
poetry install
```

2. build

```console
poe build  // using default settings, details canbe found in build.py
poe build -j 32  // multithread
```

## NOTE

We take **NO Responsibility** for the OCR results, you can open an issue when you have any errors, users should take care and check the results carefully themselves.

## TODO

- [ ] API
- [x] Desktop Deploy
- [x] ONNX
- [ ] Compile to module
- [x] Reduce package size
- [ ] Beam Search

## Developers

Any suggestions and PRs are welcome.

## Thanks

- Material Design Icons, [https://fonts.google.com/icons](https://fonts.google.com/icons)

## License

GPL-V3
[Read More](LICENSE)
