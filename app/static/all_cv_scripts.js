const initTables = async (eTable) => {
    if (!eTable.attr('id')) return
    let searching = false
    if (eTable.attr('data-searching') === 'true') {
        searching = true
    }
    if ($.fn.DataTable.isDataTable(eTable)) {
        let _x = eTable.DataTable()
        _x.clear()
        _x.destroy()
        table_gfilter_data = {}
        $.fn.dataTable.ext.search = []
    }

    let pagingType = String(eTable.attr('data-pagingType')) || 'number'
    let pageLength = parseInt(eTable.attr('data-pageLength')) || 10
    let paging = Boolean(eTable.attr('data-paging')) || false
    let dom = eTable.attr('data-dom') || 'top,bottom'
    let searchPlaceholder = eTable.attr('data-searchPlaceholder') || 'Search by Name'
    let select_search_category = eTable.attr('data-search-category') || ''
    let order = parseInt(eTable.attr('data-order-column') || 0)
    let order_direction = eTable.attr('data-order-direction') || 'desc'
    let global_fiter = eTable.attr('data-init-global-search') || false
    let listen_draw = true

    let dom_config = function () {
        var content = ""
        let category_select = ''
        if (dom.includes('top')) {
            if (select_search_category) {
                category_select = '<"select_category_block input-group justify-content-end" select<"select2_alternative_category_datatable"> >'
            }
            // content += "<'row'<'d-flex col-12 justify-content-between mb-3 mt-3'f " + category_select + ">>"
        }
        content += "<'row'<'col-sm-12'tr>>"
        if (dom.includes('bottom')) {
            content += "<'row'<'d-flex col-xl-12 justify-content-center'p><'d-flex col-xl-12 justify-content-center'i>>"
        }
        return content
    }

    let columnDefs = function (table) {
        if (!$(table).find('thead').find('th[data-filter-by-order="true"]').length) return []
        let column_def = []
        $(table).find('thead').find('th').each(function (ix, el) {
            if (!($(el).attr('data-filter-by-order') === 'true')) return
            if (($(el).attr('data-order-column') === 'true')) {
                order = ix
            }
            column_def.push({
                "targets": ix,
                data: {
                    _: `${ix}.display`,
                    sort: `${ix}.@data-order`,
                    type: `${ix}.@data-order`
                }
            })
        })
        return column_def
    }

    let visible_columns_ids = []
    let global_filter = []

    let tableDrawCallback = function (table) {
        // if (Object.keys(global_filter).length){
        //     let gfilter_dropdown = $(document).find('[data-button-filter="true"]').find('.dropdown-menu')
        //     gfilter_dropdown.html('')
        //     global_filter.forEach(function (filter_data) {
        //         table_gfilter_data = {}
        //         let select = create_gfilter_select(gfilter_dropdown, filter_data)
        //         insert_data_into_select_gfilter(table, select, filter_data, gfilter_dropdown)
        //     })
        // }
    }
    let table = eTable.DataTable({
        searching: searching,
        language: {
            search: "",
            searchPlaceholder: searchPlaceholder
        },
        fixedHeader: true,
        lengthChange: false,
        retrieve: true,
        pagingType: pagingType,
        pageLength: pageLength,
        paging: paging,
        bInfo: false,
        dom: dom_config(),
        columnDefs: columnDefs(eTable),
        drawCallback: listen_draw ? function (settings) {
            tableDrawCallback(this.api())
        } : null,
        order: [order],
    })

    table.columns().header().to$().each(function (ix, el) {
        if ($(el).index() < 0) return
        if (!$(el).attr('hidden')) {
            visible_columns_ids.push(ix)
        }
        if ((global_fiter) && ($(el).attr('data-gfilter-name'))) {
            global_filter.push({'col_id': ix, 'filter_name': $(el).attr('data-gfilter-name')})
        }
    })

    await table.search('').columns().search('').draw()

    if (Object.keys(global_filter).length) {
        let gfilter_dropdown = $(document).find('[data-button-filter="true"]').find('.dropdown-menu')
        gfilter_dropdown.html('')
        global_filter.forEach(function (filter_data) {
            table_gfilter_data = {}
            let select = create_gfilter_select(gfilter_dropdown, filter_data)
            insert_data_into_select_gfilter(table, select, filter_data, gfilter_dropdown)
        })
    }

    return table
}


$(document).ready(function (e) {
    $(document).find('table').each(function (idx, table) {
        initTables($(table))
    })
})

const show_preview_cv = (cv_manager_id) => {
    $(document).find('[data-type="show_preview"]').removeClass('d-none')
    $(document).find('[data-type="show_preview"]').addClass('d-flex')
    preview_cv(cv_manager_id)
}
