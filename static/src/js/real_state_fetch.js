odoo.define('real_state.fetch_conversations', function (require) {
    'use strict';

    // تحميل التبعيات المطلوبة
    var KanbanView = require('web.KanbanView');
    var core = require('web.core');
    var _t = core._t;

    // إضافة التعديلات إلى KanbanView
    KanbanView.include({
        /**
         * تجاوز دالة _render لجلب البيانات عند تحميل العرض.
         */
        _render: function () {
            var self = this;
            this._super.apply(this, arguments);

            // جلب البيانات عند تحميل العرض
            this._fetchData();
        },

        /**
         * دالة لجلب البيانات من الخادم.
         */
        _fetchData: function () {
            var self = this;
            this._rpc({
                model: 'conversation.management.conversation',
                method: 'fetch_conversations',
                args: [],
            }).then(function (result) {
                self.reload(); // إعادة تحميل العرض لتعكس التغييرات
            });
        },
    });
},['web.KanbanView', 'web.core']); // تعريف التبعيات هنا
