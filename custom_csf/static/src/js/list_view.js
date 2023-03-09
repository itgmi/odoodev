/** @odoo-module **/

import { ListController } from '@web/views/list/list_controller';
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class ClientNewListController extends ListController {
    async actionDef() {
        console.log(this)
        var self = this;
        this.actionService.doAction({
           type: 'ir.actions.act_window',
           res_model: 'create.csf',
           name :'create new client from CSF',
           view_mode: 'form',
           view_type: 'form',
           views: [[false, 'form']],
           target: 'new',
           res_id: false,
       });
    }
}
registry.category('views').add('client_button_tree', {
    ...listView,
    Controller: ClientNewListController,
    buttonTemplate: 'ClientNew.buttons',
});

