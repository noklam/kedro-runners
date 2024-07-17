
## How to use

Fill me in please! Don’t forget code examples:

`kedro run --runner kedro_runners.SoftFailRunner`

# Why is it useful?

> The team created a soft-fail runner to transform errors into warnings,
> allowing the pipeline to continue executing to the best of its ability
> while providing a report of any nodes that failed, so that data issues
> can be addressed. At that point, the pipeline run can be finalised by
> executing only those missing nodes separately, using appropriate Kedro
> syntax. https://kedro.org/blog/build-a-custom-kedro-runner

It’s most useful in two different scenarios: 1. Development - you want
to detect all problematic nodes in one go 2. Deployment - you want to
run as much node as you can before the Kedro pipeline is stopped.

# Why is it not in Kedro yet?

Note that the
[`SoftFailRunner`](https://noklam.github.io/kedro-softfail-runner/core.html#softfailrunner)
does not return anything, that is `result = session.run()` normally
returns a dictionary of free output, but it will be always `None` for
[`SoftFailRunner`](https://noklam.github.io/kedro-softfail-runner/core.html#softfailrunner)
due to implementation problem.

Other than that, there are no other known issues yet. In order to merge
this into the core library, this problem need to be fixed and the runner
should be test thoroughly.
