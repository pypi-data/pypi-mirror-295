import { IThemeManager } from '@jupyterlab/apputils';
/**
 * Initialization data for the @amphi/theme-light extension.
 */
const extension = {
    id: '@amphi/theme-light',
    requires: [IThemeManager],
    autoStart: true,
    activate: (app, manager) => {
        const style = '@amphi/theme-light/index.css';
        manager.register({
            name: 'Amphi Light',
            isLight: true,
            themeScrollbars: false,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    }
};
export default extension;
