Ext.ns('Ext.m3');

/**
 * @class Ext.ux.form.BaseMultiSelectFilterColumn
 * @extends Ext.m3.MultiSelectField
 *
 * Базовый класс колоночных фильтров с множественным выбором.
 * Самостоятельно не инстанцируется
 */
Ext.m3.BaseMultiSelectFilterColumn = Ext.extend(Ext.m3.MultiSelectField, {
    /**
     * Id опции Выделить все
     */
    optAllId: -5,

    /**
     * Если снято выделение со всех записей то параметр не отправляется
     */
    skipEmptyValue: true
});

Ext.reg('m3-base-multiselect-filter-column', Ext.m3.BaseMultiSelectFilterColumn);
