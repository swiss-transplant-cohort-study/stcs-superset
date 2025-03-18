function splitConfigsByBrowser(config) {
  const environments = validateBrowsers(config);
  if (environments.length) {
    const result = environments.reduce(
      ([nonIE, IE], browser) => {
        if (isIE(browser)) {
          IE.push(browser);
        } else {
          nonIE.push(browser);
        }
        return [nonIE, IE];
      },
      [[], []],
    );

    return result.reduce(
      (acc, browser) => (browser.length > 0 ? acc.concat({...config, environments: browser}) : acc),
      [],
    );
  } else {
    return [config];
  }
}

function shouldRenderIE(config) {
  return hasIE(config) && config.fakeIE;
}

function hasIE(config) {
  return validateBrowsers(config).some(isIE);
}

function isIE(browser) {
  return browser.name === 'ie' || browser.name === 'ie11';
}

function validateBrowsers(config) {
  if (config.environments) {
    return Array.isArray(config.environments) ? config.environments : [config.environments];
  } else {
    return [];
  }
}

module.exports = {splitConfigsByBrowser, shouldRenderIE, isIE};
