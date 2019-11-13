# BenchBot Examples

This package shows some simple examples for using the BenchBot API in the ACRV Semantic Scene Understanding Challenge. See [benchbot_devel](https://bitbucket.org/acrv/benchbot_devel/src/master/) for getting BenchBot up & running on your system.

Examples can be run natively:

```bash
python hello_benchbot/hello_benchbot
```

```bash
./hello_benchbot/hello_benchbot
```

or inside a container using the provided Dockerfiles (as will be required to submit to the challenge):

```bash
cd hello_benchbot; docker build; docker run
```

**Note: all of these running methods are wrapped by the `benchbot_submit` script & associated methods in [benchbot_devel](https://bitbucket.org/acrv/benchbot_devel/src/master/); use that instead of running the commands here (otherwise your BenchBot solution won't have a simulator to interact with)!**
