$(document).ready(function() {
    // Inicializar DataTable para la vista de lista
    if ($('#seccionFichaTable').length) {
        var table = $('#seccionFichaTable').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.3.0/i18n/es-CL.json'
            }
        });
    }

    // Verificar si estamos en la página de creación/edición
    if ($('#especificaciones-container').length) {
        // Ejecutar la numeración inicial
        renumerarFilas();
        
        console.log("Formulario de especificaciones detectado");
        
        // Comprobar el nombre del campo TOTAL_FORMS
        var totalFormsField = $('input[name$="TOTAL_FORMS"]').first();
        console.log("Campo TOTAL_FORMS encontrado:", totalFormsField.attr('name'));
    }

    // Función para renumerar todas las filas
    function renumerarFilas() {
        $('#especificaciones-container tr.especificacion-form:visible').each(function(index) {
            var numero = index + 1;
            $(this).find('.orden-numero').text(numero);
            $(this).find('.orden-input').val(numero);
        });
    }
    
    // Función para agregar nueva especificación (por fila)
    $(document).on('click', '.add-especificacion', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("Botón agregar especificación clickeado");
        
        // Buscar el campo TOTAL_FORMS sin asumir un prefijo específico
        var totalFormsField = $('input[name$="TOTAL_FORMS"]').first();
        var prefix = totalFormsField.attr('name').replace('-TOTAL_FORMS', '');
        
        console.log("Prefijo del formset:", prefix);
        var formCount = parseInt(totalFormsField.val());
        console.log("Número actual de formularios:", formCount);
        
        var $lastRow = $('#especificaciones-container tr.especificacion-form:last');
        var $newRow = $lastRow.clone(true);
        
        // Actualizar IDs y nombres con el nuevo índice
        $newRow.find('input, select').each(function() {
            var name = $(this).attr('name');
            if (name) {
                name = name.replace(new RegExp(prefix + '-(\\d+)-'), prefix + '-' + formCount + '-');
                var id = 'id_' + name;
                $(this).attr({'name': name, 'id': id});
                
                // Limpiar valores
                if (!$(this).is(':checkbox')) {
                    $(this).val('');
                } else {
                    $(this).prop('checked', false);
                }
            }
        });
        
        // Añadir la nueva fila
        $('#especificaciones-container').append($newRow);
        
        // Incrementar el contador de formularios
        totalFormsField.val(formCount + 1);
        
        // Renumerar las filas después de agregar
        renumerarFilas();
        
        console.log("Nueva fila agregada, total ahora:", totalFormsField.val());
        return false;
    });

    // Función para eliminar especificación (por fila)
    $(document).on('click', '.delete-especificacion', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log("Botón eliminar especificación clickeado");
        
        var totalRows = $('#especificaciones-container tr.especificacion-form:visible').length;
        console.log("Filas actuales:", totalRows);
        
        if (totalRows > 1) {
            var $row = $(this).closest('tr.especificacion-form');
            
            // Si es un formulario existente, marcarlo para DELETE en lugar de eliminar
            var $deleteInput = $row.find('input[name$="-DELETE"]');
            if ($deleteInput.length) {
                $deleteInput.prop('checked', true);
                $row.hide();
                console.log("Fila existente marcada para eliminar");
            } else {
                $row.remove();
                console.log("Fila nueva removida del DOM");
            }
            
            // Renumerar las filas después de eliminar
            renumerarFilas();
        } else {
            alert("Debe haber al menos una especificación");
            console.log("No se puede eliminar la única fila existente");
        }
        return false;
    });

    // Limpiar formulario al cerrar modal de creación
    $('#crearModal').on('hidden.bs.modal', function() {
        $('#form-add-seccion')[0].reset();
        $('#form-add-seccion input[type=checkbox]').prop('checked', false);
        // Limpiar especificaciones
        $('.especificacion-form:not(:first)').remove();
        $('#id_especificaciones-TOTAL_FORMS').val('1');
    });

    // Manejar envío del formulario de creación
    $('#form-add-seccion').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            url: '/maq_fichatecnica/seccion-ficha/crear/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    alert(response.message || 'Error al crear la sección');
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
        var seccion = $(this).data('seccion');
        var tipoeqs = $(this).data('tipoeq').split(',').filter(Boolean);
        var especificaciones = $(this).data('especificaciones');

        $('#edit-id-seccion').val(id);
        $('#edit-seccion').val(seccion);
        $('#edit-tipoeq-checkboxes input[type=checkbox]').prop('checked', false);
        tipoeqs.forEach(function(tipoid) {
            $('#edit-tipoeq-' + tipoid).prop('checked', true);
        });

        // Limpiar y cargar especificaciones
        $('.especificacion-form:not(:first)').remove();
        if (especificaciones && especificaciones.length > 0) {
            especificaciones.forEach(function(esp, index) {
                if (index > 0) {
                    $('#add-especificacion').click();
                }
                var form = $('.especificacion-form').eq(index);
                form.find('[name$="-especificacion"]').val(esp.especificacion);
                form.find('[name$="-tipodato"]').val(esp.tipodato);
                form.find('[name$="-unidadmedida"]').val(esp.unidadmedida);
            });
        }
    });

    // Limpiar formulario al cerrar modal de edición
    $('#editModal').on('hidden.bs.modal', function() {
        $('#form-edit-seccion')[0].reset();
        $('#edit-tipoeq-checkboxes input[type=checkbox]').prop('checked', false);
        $('.especificacion-form:not(:first)').remove();
        $('#id_especificaciones-TOTAL_FORMS').val('1');
    });

    // Manejar envío del formulario de edición
    $('#form-edit-seccion').on('submit', function(e) {
        e.preventDefault();
        var id = $('#edit-id-seccion').val();
        $.ajax({
            url: '/maq_fichatecnica/seccion-ficha/' + id + '/editar/',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#edit-message').html(response.message || 'Error al actualizar la sección')
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
        $('#delete-id-seccion').val(id);
    });

    // Manejar confirmación de eliminación
    $('#confirm-delete-seccion').click(function() {
        var id = $('#delete-id-seccion').val();
        $.ajax({
            url: '/maq_fichatecnica/seccion-ficha/' + id + '/eliminar/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    location.reload();
                } else {
                    $('#deleteModal').modal('hide');
                    alert(response.message || 'Error al eliminar la sección');
                }
            },
            error: function(xhr, status, error) {
                $('#deleteModal').modal('hide');
                alert('Error al comunicarse con el servidor: ' + error);
            }
        });
    });
});