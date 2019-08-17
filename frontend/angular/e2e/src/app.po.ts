import { browser, by, element } from 'protractor';

export class AppPage {
  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  getBrandText() {
    return element(by.css('app-root .brand')).getText() as Promise<string>;
  }
}
