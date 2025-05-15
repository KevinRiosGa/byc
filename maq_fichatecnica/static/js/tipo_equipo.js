
$(document).ready(function() {
    // Inicializar DataTable
    var table = $('#tipoEquipoTable').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
        }
    });
    
    // Limpiar formulario al cerrar modal de creación
    $('#crearModal').on('hidden.bs.modal', function() {
        $('#form-add')[0].reset();
    });

    // Manejar envío del formulario de creación
    $('#form-add').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/maq_fichatecnica/tipo_equipo/crear/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert(response.message || 'Error al crear el tipo de equipo');
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
        var prefixeq = $(this).data('prefixeq');
        var tipoeq = $(this).data('tipoeq');

        $('#edit-id').val(id);
        $('#edit-prefixeq').val(prefixeq).prop('disabled', true);
        $('#edit-tipoeq').val(tipoeq);
    });

    // Limpiar y habilitar el campo prefijo al cerrar el modal de edición
    $('#editModal').on('hidden.bs.modal', function() {
        $('#edit-prefixeq').prop('disabled', false);
        $('#form-edit')[0].reset();
    });

    // Manejar envío del formulario de edición
    $('#form-edit').on('submit', function(e) {
        e.preventDefault();
        var id = $('#edit-id').val();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        
        $.ajax({
            url: '/maq_fichatecnica/tipo_equipo/' + id + '/editar/',
            type: 'POST',
            data: {
                prefixeq: $('#edit-prefixeq').val(),
                tipoeq: $('#edit-tipoeq').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#edit-message').html(response.message || 'Error al actualizar el tipo de equipo')
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
        $('#delete-id').val(id);
    });

    // Manejar confirmación de eliminación
    $('#confirm-delete').click(function() {
        var id = $('#delete-id').val();
        $.ajax({
            url: '/maq_fichatecnica/tipo_equipo/' + id + '/eliminar/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    // Mostrar mensaje de error en un modal
                    $('#deleteModal').modal('hide');
                    alert((response.message ? response.message : 'Error al eliminar el tipo de equipo') + (response.traceback ? '\n' + response.traceback : ''));
                }
            },
            error: function(xhr, status, error) {
                $('#deleteModal').modal('hide');
                alert('Error al comunicarse con el servidor: ' + error);
            }
        });
    });
}); 