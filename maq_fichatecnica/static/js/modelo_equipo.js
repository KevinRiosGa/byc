function cargarMarcasPorTipo(tipoId, $selectMarca, marcaSeleccionada) {
    $selectMarca.html('<option value="">Cargando...</option>');
    $.get('/maq_fichatecnica/ajax/marcas_por_tipo/', { tipo_id: tipoId }, function(data) {
        $selectMarca.empty();
        if (data.marcas.length === 0) {
            $selectMarca.append('<option value="">No hay marcas disponibles</option>');
        } else {
            $selectMarca.append('<option value="">Seleccione una marca</option>');
            data.marcas.forEach(function(marca) {
                var selected = marcaSeleccionada && marcaSeleccionada == marca.id ? 'selected' : '';
                $selectMarca.append('<option value="' + marca.id + '" ' + selected + '>' + marca.nombre + '</option>');
            });
        }
    });
}

// Crear
$('#id_tipoeq').change(function() {
    var tipoId = $(this).val();
    cargarMarcasPorTipo(tipoId, $('#id_marcaeq'));
});

// Editar
$('#edit-tipoeq').change(function() {
    var tipoId = $(this).val();
    cargarMarcasPorTipo(tipoId, $('#edit-marcaeq'));
});

$(document).ready(function() {
    // Inicializar DataTable
    var table = $('#modeloEquipoTable').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.3.0/i18n/es-CL.json'
        }
    });

    // Limpiar formulario al cerrar modal de creación
    $('#crearModal').on('hidden.bs.modal', function() {
        $('#form-add-modelo')[0].reset();
        $('#id_marcaeq').empty().append('<option value="">Seleccione una marca</option>');
    });

    // Manejar envío del formulario de creación
    $('#form-add-modelo').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/maq_fichatecnica/modelo_equipo/crear/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert(response.message || 'Error al crear el modelo');
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
        var tipoeq = $(this).data('tipoeq');
        var marcaeq = $(this).data('marcaeq');
        var modeloeq = $(this).data('modeloeq');

        $('#edit-id-modelo').val(id);
        $('#edit-tipoeq').val(tipoeq);
        cargarMarcasPorTipo(tipoeq, $('#edit-marcaeq'), marcaeq);
        $('#edit-modeloeq').val(modeloeq);
    });

    // Limpiar formulario al cerrar modal de edición
    $('#editModal').on('hidden.bs.modal', function() {
        $('#form-edit-modelo')[0].reset();
    });

    // Manejar envío del formulario de edición
    $('#form-edit-modelo').on('submit', function(e) {
        e.preventDefault();
        var id = $('#edit-id-modelo').val();
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: '/maq_fichatecnica/modelo_equipo/' + id + '/editar/',
            type: 'POST',
            data: {
                tipoeq: $('#edit-tipoeq').val(),
                marcaeq: $('#edit-marcaeq').val(),
                modeloeq: $('#edit-modeloeq').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#edit-message').html(response.message || 'Error al actualizar el modelo')
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
        $('#delete-id-modelo').val(id);
    });

    // Manejar confirmación de eliminación
    $('#confirm-delete-modelo').click(function() {
        var id = $('#delete-id-modelo').val();
        $.ajax({
            url: '/maq_fichatecnica/modelo_equipo/' + id + '/eliminar/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#deleteModal').modal('hide');
                    alert(response.message || 'Error al eliminar el modelo');
                }
            },
            error: function(xhr, status, error) {
                $('#deleteModal').modal('hide');
                alert('Error al comunicarse con el servidor: ' + error);
            }
        });
    });
}); 