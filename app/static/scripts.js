const show_curent_step = (step) => {
    $(document).find('.progress-item.active').removeClass('active')
    $(document).find(`.progress-item[data-step="${step}"]`).addClass('active')
}



const preview_cv = async (cv_manager_id) => {
    let request = await fetch(`/cv_manager/cv_preview/${cv_manager_id}?preview_mode=True`)
    let response = await request.json()
    var $iframe = $(document).find('#preview_cv');
    $iframe.ready(function() {
        let html_response = $(response.html)
        $(html_response).find('*').css('pointer-events', 'none')
        $iframe.contents().find("body").html(html_response);
    });
}

class SortableEntities {
    constructor() {
        this.entities_length = []
        this.deleted_entities_length = []
        this.block = null
        this.sortable = null
    }

    get_order(elements, array_to_push_order = null){
        let self = this
        $.each(elements, function (order, element) {
            let current_order = order + 1
            if (current_order == 1){
                $(element).find('.remove_block').hide()
            }
            $(element).find('input').each(function (idx, ele){
                let name = $(ele).attr('data-name')
                $(ele).attr('name',`${current_order}_${name}`)
            })
            $(element).find('textarea').each(function (idx, ele){
                let name = $(ele).attr('data-name')
                $(ele).attr('name',`${current_order}_${name}`)
            })
            $(element).attr('data-order', current_order)
            array_to_push_order.push(parseInt($(element).attr('data-order')))
        })
        // console.log(this.entities_length)
        $(this.form).find('[name="last_related_count"]').val(this.entities_length)
    }

    make_update() {
        this.entities_length = []
        this.get_order($(this.block).find('.this_block'), this.entities_length)
        $(this.form).find('[name="last_related_count"]').val(this.entities_length)
    }

    add_new_instance() {
        let next_count = this.next_entity_count()
        this.entities_length.push(next_count)
        this.make_update()
    }

    next_entity_count() {
        if (this.deleted_entities_length.length) {
            return this.deleted_entities_length.pop()
        } else {
            return $(this.block).find('.this_block').length + 1
        }
    }

    init_sortable(block) {
        let self = this
        this.form = $(block).closest('form')
        this.entities_length = []

        this.block = $(block).sortable({
            cursor: "move",
            axis: "y",
            handle: '.handle_drag',
            opacity: 0.5,
            tolerance: "pointer",
            placeholder: "ui-state-highlight",
            create: function (event, ui) {
                self.get_order($(block).find('.this_block'), self.entities_length)
                self.deleted_entities_length = []
            },
            update : function (event, ui) {
                self.make_update()
            },
        })
    }

    remove_instancecc(element) {
        let to_delete_key = $(element).attr('data-order')
        this.deleted_entities_length.push(parseInt(to_delete_key))
        this.deleted_entities_length.sort()
        this.deleted_entities_length.reverse()
        $(element).remove()
        this.make_update()
    }
}

sortable_func = new SortableEntities()

async function fetchBlob(url) {
    const response = await fetch(url);

    // Here is the significant part
    // reading the stream as a blob instead of json
    return response.blob();
}
const inset_file_in_input = () => {
    if($(document).find('[data-type="upload_cv_form"]').find('input[type="file"]')){
        $(document).find('[data-type="upload_cv_form"]').find('input[type="file"]').each(async function (idx, elem){
            let file_reader = new FileReader()
            let url = $(elem).attr('data-value')
            let imageBlob = await fetchBlob(url)
            file_reader.readAsDataURL(imageBlob)
            elem.file = file_reader
        })
    }
}

const change_step = async (step) => {
    let cv_manager_id = $(document).find('[data-type="upload_cv_form"]').attr('data-instance-id')
    let uri = new URLSearchParams({
        cv_manager_id: cv_manager_id
    })
    let request = await fetch(`/cv_manager/change_step/${step}?`+uri)
    let response = await request.json()
    $(document).find('[data-type="upload_cv_form"]').html(response.form)
    sortable_func.init_sortable(($(document).find('[data-sortable="true"]')))
    show_curent_step(response.current_step)
    preview_cv(cv_manager_id)
    inset_file_in_input()
}

const get_next_step = async (step) => {
    let cv_manager_id = $(document).find('[data-type="upload_cv_form"]').attr('data-instance-id')
    let uri = new URLSearchParams({
        cv_manager_id: cv_manager_id
    })
    let request = await fetch(`/cv_manager/get_next_step/${step}?`+uri)
    let response = await request.json()
    $(document).find('[data-type="upload_cv_form"]').html(response.form)
    sortable_func.init_sortable(($(document).find('[data-sortable="true"]')))
    show_curent_step(response.current_step)
    preview_cv(cv_manager_id)
    inset_file_in_input()
}

const formToObject = (formData, raise_exception = true) => {
    let formEntries = formData.entries()
    var has_error = false
    var errors = {}

    function ValidationError(errors) {
        this.errors = errors
    }

    let getValue = function (k, v) {
        return v
    }

    let data = Array.from(formEntries).reduce((acc, [k, v]) => {
        if (k.includes('[]')) {
            if (!(k.replace('[]', '') in acc)) {
                acc[k.replace('[]', '')] = []
            }
            acc[k.replace('[]', '')].push(getValue(k, v))
        } else {
            acc[k] = getValue(k, v);
        }
        return acc
    }, {})
    if (has_error && raise_exception) throw new ValidationError(errors)
    return data
}


$(document).on('submit', 'form', async function (e) {
    e.preventDefault()
    e.stopPropagation()


    let data = null
    let form = $(this)

    if($(form).find('input[type="file"]')){
        data = new FormData($(this).get(0))
        // data.forEach(function (idx, val) {
        //     console.log(idx, val)
        // })
    }else {
        data = form.serialize()
    }
    let method = $(this).attr('method')
    let url = $(this).attr('action')
    $.ajax({
        url: url,
        method: method,
        cache: false,
        processData: false,
        // contentType: 'application/json; charset=utf-8',
        contentType: false,
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        data: data,
        success: function (data) {
            let current_step = $(form).attr('data-current-step')
            let to_change = $(form).attr('data-change-step')

            if(to_change){
                get_next_step(current_step)
            }
        }
    })
})

const remove_block = (btn) => {
    sortable_func.remove_instancecc($(btn).closest('.this_block'))
}

const add_new_experience = () => {
    let html = `
        <div class="col-12 experience-block this_block position-relative">
            <div class="handle_drag"><i class="fa-solid fa-arrows-up-down-left-right"></i></div>
            <div class="remove_block" onclick="remove_block($(this))"><i class="fa-solid fa-trash"></i></div>
            <div class="col-12">
                <label for="experience_name" class="form-label">Experience name:</label>
                <input required type="text" data-name="name" name="name" class="form-control">
            </div>
            <div class="col-12">
                <label for="experience_details" class="form-label">Details:</label>
                <textarea data-name="details" name="details" id="" cols="30" rows="5" class="form-control"></textarea>
            </div>
        </div>
    `
    let element = $(html)
    $(document).find('form').find('[data-action="upload_experiences"]').append(element)
    sortable_func.add_new_instance()
}

const add_new_education = () => {
    let html = `
        <div class="col-12 education-block this_block position-relative">
            <div class="handle_drag"><i class="fa-solid fa-arrows-up-down-left-right"></i></div>
            <div class="remove_block" onclick="remove_block($(this))"><i class="fa-solid fa-trash"></i></div>
            <div class="col-12">
                <label for="education_name" class="form-label">Education:</label>
                <input required type="text" data-name="name" name="name" class="form-control">
            </div>
            <div class="col-12">
                <label for="education_city" class="form-label">City:</label>
                <input required type="text" data-name="city" name="city" class="form-control">
            </div>
            <div class="col-12">
                <label for="details" class="form-label">Details:</label>
                <textarea name="details" data-name="details" id="" cols="30" rows="5" class="form-control"></textarea>
            </div>
        </div>
    `
    let element = $(html)
    $(document).find('form').find('[data-action="upload_education"]').append(element)
    sortable_func.add_new_instance()
}

const add_new_skill = () => {
    let html = `
        <div class="col-12 skill-block this_block position-relative">
            <div class="handle_drag"><i class="fa-solid fa-arrows-up-down-left-right"></i></div>
            <div class="remove_block" onclick="remove_block($(this))"><i class="fa-solid fa-trash"></i></div>
            <div class="col-12">
                <label for="skill" class="form-label">Skill:</label>
                <input required type="text" data-name="skill" name="skill" class="form-control">
            </div>
            <div class="col-12">
                <label for="point" class="form-label">Point:</label>
                <input required type="range" value="0" min="0" max="5" step="1" data-name="point" name="point" class="form-range form-control">
            </div>
        </div>
    `
    let element = $(html)
    $(document).find('form').find('[data-action="upload_skill"]').append(element)
    sortable_func.add_new_instance()
}
