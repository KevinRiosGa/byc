$(document).ready(function() {
    // Inicializar DataTable
    var table = $('#marcaEquipoTable').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.3.0/i18n/es-CL.json'
        }
    });

    // Limpiar formulario al cerrar modal de creación
    $('#crearModal').on('hidden.bs.modal', function() {
        $('#form-add-marca')[0].reset();
        $('#form-add-marca input[type=checkbox]').prop('checked', false);
    });

    // Manejar envío del formulario de creación
    $('#form-add-marca').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/maq_fichatecnica/marca_equipo/crear/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert(response.message || 'Error al crear la marca');
                }
            },
            error: function() {
                alert('Error al comunicarse con el servidor');
            }
        });
    });

    // Manejar clic en botón de editar
    $('.edit-btn').click(function() {
        var id = $(this).data('id');
        var marcaeq = $(this).data('marcaeq');
        var tipoeqs = $(this).data('tipoeq').split(',').filter(Boolean);

        $('#edit-id-marca').val(id);
        $('#edit-marcaeq').val(marcaeq);
        $('#edit-tipoeq-checkboxes input[type=checkbox]').prop('checked', false);
        tipoeqs.forEach(function(tipoid) {
            $('#edit-tipoeq-' + tipoid).prop('checked', true);
        });
    });

    // Limpiar formulario al cerrar modal de edición
    $('#editModal').on('hidden.bs.modal', function() {
        $('#form-edit-marca')[0].reset();
        $('#edit-tipoeq-checkboxes input[type=checkbox]').prop('checked', false);
    });

    // Manejar envío del formulario de edición
    $('#form-edit-marca').on('submit', function(e) {
        e.preventDefault();
        var id = $('#edit-id-marca').val();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        var tipoeqs = [];
        $('#edit-tipoeq-checkboxes input[type=checkbox]:checked').each(function() {
            tipoeqs.push($(this).val());
        });
        $.ajax({
            url: '/maq_fichatecnica/marca_equipo/' + id + '/editar/',
            type: 'POST',
            data: {
                marcaeq: $('#edit-marcaeq').val(),
                tipoeq: tipoeqs,
                csrfmiddlewaretoken: csrfToken
            },
            traditional: true,
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#edit-message').html(response.message || 'Error al actualizar la marca')
                        .removeClass('alert-success alert-danger')
                        .addClass('alert-danger')
                        .show();
                }
            },
            error: function(xhr, status, error) {
                $('#edit-message').html('Error al comunicarse con el servidor: ' + error)
                    .removeClass('alert-success alert-danger')
                    .addClass('alert-danger')
                    .show();
            }
        });
    });

    // Manejar clic en botón de eliminar
    $('.delete-btn').click(function() {
        var id = $(this).data('id');
        $('#delete-id-marca').val(id);
    });

    // Manejar confirmación de eliminación
    $('#confirm-delete-marca').click(function() {
        var id = $('#delete-id-marca').val();
        $.ajax({
            url: '/maq_fichatecnica/marca_equipo/' + id + '/eliminar/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#deleteModal').modal('hide');
                    alert(response.message || 'Error al eliminar la marca');
                }
            },
            error: function(xhr, status, error) {
                $('#deleteModal').modal('hide');
                alert('Error al comunicarse con el servidor: ' + error);
            }
        });
    });
}); 