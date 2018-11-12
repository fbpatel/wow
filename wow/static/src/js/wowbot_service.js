odoo.define('mail_bot.WowBotService', function (require) {
"use strict";

var AbstractService = require('web.AbstractService');
var core = require('web.core');
var session = require('web.session');

var _t = core._t;

var WowBotService =  AbstractService.extend({
    /**
     * @override
     */
    start: function () {
        var self = this;
        if ('wow_initialized' in session && ! session.wow_initialized) {
            setTimeout(function () {
                session.wow_initialized = true;
                self._rpc({
                    model: 'mail.channel',
                    method: 'init_wow',
                });
            }, 5*60*1000);
        }
    },
});

core.serviceRegistry.add('wowbot_service', WowBotService);
return WowBotService;

});
