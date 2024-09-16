odoo.define('your_module.notification_button', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');

    var NotificationButton = Widget.extend({
        template: 'UserMenu',
        events: {
            'click .o_external_notifications': '_onNotificationClick',
        },

        _onNotificationClick: function () {
            // هنا يجب أن تقوم بجلب الإشعارات من المصدر الخارجي
            // مثلا عن طريق AJAX أو أي وسيلة أخرى
            this._fetchNotifications();
        },

        _fetchNotifications: function () {
            var self = this;
            $.ajax({
                url: 'https://external-api.com/notifications',  // رابط المصدر الخارجي
                method: 'GET',
                success: function (data) {
                    // يمكنك معالجة البيانات هنا، وربما تخزينها في موديل الإشعارات
                    console.log(data);
                },
                error: function () {
                    console.error('Failed to fetch notifications');
                }
            });
        },
    });

    SystrayMenu.Items.push(NotificationButton);

    return NotificationButton;
});
