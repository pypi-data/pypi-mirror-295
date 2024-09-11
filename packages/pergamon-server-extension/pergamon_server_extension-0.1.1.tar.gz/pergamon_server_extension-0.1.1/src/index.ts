import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {INotebookTracker} from '@jupyterlab/notebook';

/**
 * Initialization data for the pergamon_server_extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pergamon_server_extension:plugin',
  description: 'Calliope server extension',
  requires: [INotebookTracker],
  autoStart: true,
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {
    console.log('JupyterLab extension pergamon_server_extension is activated!');

    tracker.widgetAdded.connect((sender, notebookPanel) => {
      notebookPanel.sessionContext.ready.then(() => {
        const session = notebookPanel.sessionContext.session;
        if (session?.kernel) {
          session.kernel.requestExecute({
            code: '%load_ext jupyter_ai'
          });
        }
      });
    });
  }
};

export default plugin;
