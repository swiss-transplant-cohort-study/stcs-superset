'use strict';
const chalk = require('chalk');

module.exports = chalk.yellow(`
Important notice: Your Applitools visual tests are currently running with a concurrency value of 5.
This means that only up to 5 visual tests can run in parallel, and therefore the execution might be slower.
If your Applitools license supports a higher concurrency level, set the "testConcurrency" parameter as explained here: https://applitools.com/docs/api-ref/sdk-api/storybook/config.
Need a higher concurrency in your account? Email us @ sdr@applitools.com with your required concurrency level.
`);
