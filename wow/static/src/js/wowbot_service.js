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
            console.log('start timeout');
            setTimeout(function () {
                console.log('init_wow');
                session.wow_initialized = true;
                self._rpc({
                    model: 'mail.channel',
                    method: 'init_wow',
                });
            }, 5*60*1000);
        }
    },
    /**
     * Get the previews related to the OdooBot (conversation not included).
     * For instance, when there is no conversation with OdooBot and OdooBot has
     * a request, it should display a preview in the systray messaging menu.
     *
     * @param {string|undefined} [filter]
     * @returns {Object[]} list of objects that are compatible with the
     *   'mail.Preview' template.
     */
    getPreviews: function (filter) {
        var previews = [];
        if (this.hasRequest() && (filter === 'mailbox_inbox' || !filter)) {
            previews.push({
                title: _t("OdooBot has a request"),
                imageSRC: "/mail/static/src/img/odoobot.png",
                status: 'bot',
                body:  _t("Enable desktop notifications to chat"),
                id: 'request_notification',
                unreadCounter: 1,
            });
        }
        return previews;
    },
    /**
     * Tell whether OdooBot has a request or not.
     *
     * @returns {boolean}
     */
    hasRequest: function () {
        return window.Notification && window.Notification.permission === "default";
    },
});

core.serviceRegistry.add('wowbot_service', WowBotService);
return WowBotService;

});
