import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

/**
 * Initialization data for the pergamon_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pergamon_theme:plugin',
  description: 'Pergamon Theme Extension.',
  autoStart: true,
  requires: [IThemeManager],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension pergamon_theme is activated!');
    const style = 'pergamon_theme/index.css';

    manager.register({
      name: 'pergamon_theme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });

    manager.setTheme('pergamon_theme');

    setTimeout(() => {
      const bottomBarLeft =
        document.getElementsByClassName('jp-StatusBar-Left')[0];

      // apply simple UI
      if (bottomBarLeft) {
        const switchElement =
          bottomBarLeft.getElementsByClassName('jp-switch')[0];

        if (switchElement.getAttribute('aria-checked') === 'false') {
          switchElement?.dispatchEvent(new Event('click'));
        }

        bottomBarLeft?.parentNode?.removeChild(bottomBarLeft);
      }

      [
        document.getElementsByClassName('jp-StatusBar-Right')[0], // bottom right section
        document.querySelector(
          '.jp-mod-right [data-id="jp-property-inspector"]'
        ), // elements from the left bar
        document.querySelector('.jp-mod-right [data-id="jp-debugger-sidebar"]'), // elements from the left bar
        document.querySelector('#jp-title-panel-title') // default title
      ].forEach(element => {
        element?.parentNode?.removeChild(element);
      });
    }, 500);

    // Create a custom loading screen element
    const customLoadingScreen = document.createElement('div');
    customLoadingScreen.className = 'custom-loading-screen';
    customLoadingScreen.textContent = 'Loading, please wait...';

    // Add the custom loading screen to the document
    document.body.appendChild(customLoadingScreen);

    const splashElement = document.querySelector('.jp-Splash');
    if (splashElement) {
      splashElement.remove();
    }

    // Remove the custom loading screen once JupyterLab is fully loaded
    app.restored.then(() => {
      document.body.removeChild(customLoadingScreen);
    });
  }
};

export default plugin;
