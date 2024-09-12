import json
import traceback
import requests

def setLogSistema(log_params, log, type_log,  set_log_sistema):
    """
    Esta función se encarga de setear el log en el sistema y en la base de datos
    """
    set_log_sistema(
        log_params.view,
        log_params.method,
        log_params.function, 
        log,	
        log_params.params,
        type_log,
        log_params.trace,
        log_params.stack
    )

class statusClass: 
    HTTP_404_NOT_FOUND = 404
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_400_BAD_REQUEST = 400


def firma_electronica_avanzada(
    ficha_id, 
    log_sistema,
    set_log_sistema,
    models,
    constants,
    settings,
    obtiene_titular_representante_proyecto,
    get_fecha_vencimiento_evaluacion,
    date_to_str_local,
    responsable_departamento_exedoc,
    estado_evaluacion=None, 
    prorroga=False, 
    borrador=None,
    tipo_de_envio=None
): 
    """
    Firma Electrónica Avanzada

    Argumentos
    ----------
    - ``ficha_id`` (str) : id de la ficha
    - ``log_sistema`` (SeimLogSistema) : objeto de SeimLogSistema
    - ``set_log_sistema`` (function) : función de set_log_sistema para escribir en el log del sistema
    - ``models`` : objeto de models
    - ``constants`` : objeto de constants
    - ``settings`` : objeto de settings
    - ``obtiene_titular_representante_proyecto`` (function) : función para obtener el titular y el representante del proyecto
    - ``get_fecha_vencimiento_evaluacion`` (function) : función para obtener la fecha de vencimiento de la evaluación
    - ``date_to_str_local`` (function) : función para convertir una fecha a string
    - ``responsable_departamento_exedoc`` (function) : función para obtener el responsable del departamento de exedoc
    - ``estado_evaluacion`` (int) : estado de la evaluación
    - ``prorroga`` (bool) : si es una prórroga
    - ``borrador`` (Archivo) : objeto de Archivo
    - ``tipo_de_envio`` (str) : tipo de envío {None, 'GENERAR_RESOLUCION', 'EVALUACION IMIV_3'}

    Info
    ----
    - el argumento ``set_log_sistema`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.set_log_sistema import set_log_sistema
    
    - el argumento ``obtiene_titular_representante_proyecto`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.obtiene_titular_representante_proyecto import obtiene_titular_representante_proyecto

    - el argumento ``get_fecha_vencimiento_evaluacion`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.get_fecha_vencimiento_evaluacion import get_fecha_vencimiento_evaluacion
    
    - el argumento ``date_to_str_local`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.date_to_str_local import date_to_str_local

    - el argumento ``responsable_departamento_exedoc`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.responsable_departamento_exedoc import responsable_departamento_exedoc

    Retorno
    -------
    - ``data`` (dict) : diccionario con la respuesta de la llamada a EXEDOC
    - ``status`` (int) : el estado de la respuesta
    - ``URL_GDMTT`` (str|None) : la url de la llamada a EXEDOC

    """
    print("Estoy en firma electronica avanzada")
    log_sistema \
        .add_params('ficha_id', ficha_id) \
        .add_params('estado_evaluacion', estado_evaluacion) \
        #.info('Inicia función de firma electrónica avanzada')
        
    print('ficha_id:', ficha_id, '- estado_evaluacion:', estado_evaluacion)
    setLogSistema(log_sistema, 'Inicia función de firma electrónica avanzada', 'INFO', set_log_sistema)
    
    if not models.Ficha.objects.filter(id=ficha_id).exists():
        print("Ficha no existe")
        #log_sistema.error("La ficha no existe")
        raise models.Ficha.DoesNotExist
        
    o_ficha = models.Ficha.objects.get(id=ficha_id)
    log_sistema.add_params("o_ficha", o_ficha)

    print(f'o_ficha.id: {o_ficha.id} - o_ficha.tipo_ficha: {o_ficha.tipo_ficha}')

    if not models.Evaluacion_Imiv.objects.filter(imiv_id=o_ficha.id, vigente=True).exists():
        print("La evaluacion no existe")
        #log_sistema.error("La evaluacion no existe")
        raise models.Evaluacion_Imiv.DoesNotExist

    #print("Sali de los if de firma electrónica avanzada")
    o_evaluacion = models.Evaluacion_Imiv.objects.get(imiv_id=o_ficha.id, vigente=True)
    print(f'o_evaluacion.imiv.tipo_imiv_id: {o_evaluacion.imiv.tipo_imiv_id} ')
    #log_sistema.info("firma_electronica_avanzada: se encontró la evaluacion")
    setLogSistema(log_sistema, "firma_electronica_avanzada: se encontró la evaluacion", 'INFO', set_log_sistema)

    tipo_documento_seim = None
    if prorroga:
        #print("Estoy en el if de prórroga")
        tipo_documento_seim = models.TipoDocumentoSeim.RESPRORE
        log_sistema \
            .add_params("es_prorroga", True)

    elif not models.EstadoEvaluacion.objects.filter(id=estado_evaluacion).exists():
        print("El estado de evaluacion no existe")
        #log_sistema.error("El estado de evaluacion no existe")
        raise models.EstadoEvaluacion.DoesNotExist

    else:
        #print("Estoy en el if de estado evaluacion")
        if estado_evaluacion == models.EstadoEvaluacion.RESOLUCION_OBSERVADO:
            log_sistema.add_params("es_observado", True)
            if o_evaluacion.imiv.tipo_imiv_id == models.TipoIMIV.TIPO_IMIV_INFORME_SUFICIENCIA:
                tipo_documento_seim = constants.DOCTO_SEIM_RESOLUCION_SUFICIENCIA_OBSERVA
            else:
                tipo_documento_seim = models.TipoDocumentoSeim.RESEVAOBS if o_ficha.tipo_ficha == constants.TIPO_FICHA_SIMPLE else \
                    models.TipoDocumentoSeim.RESEVAOBC
        elif estado_evaluacion in [models.EstadoEvaluacion.RESOLUCION_APROBADO, models.EstadoEvaluacion.RESOLUCION_RECHAZADO]:
            if o_evaluacion.imiv.tipo_imiv_id == models.TipoIMIV.TIPO_IMIV_INFORME_SUFICIENCIA:
                tipo_documento_seim = constants.DOCTO_SEIM_RESOLUCION_SUFICIENCIA_APRUEBA_RECHAZA
            else:
                tipo_documento_seim = models.TipoDocumentoSeim.RESSEREVA if o_ficha.tipo_ficha == constants.TIPO_FICHA_SIMPLE else \
                    models.TipoDocumentoSeim.RESEVAC
        elif estado_evaluacion == models.EstadoEvaluacion.RESOLUCION_DESISTIDO:
            tipo_documento_seim = models.TipoDocumentoSeim.RESDES
        elif estado_evaluacion == models.EstadoEvaluacion.RECHAZADO_NO_CORRECCION:
            tipo_documento_seim = models.TipoDocumentoSeim.RESNOCOS
        else:
            #log_sistema.error("Estado de evaluación no implementado para firma electrónica avanzada")
            setLogSistema(log_sistema, "Estado de evaluación no implementado para firma electrónica avanzada", 'ERROR', set_log_sistema)
            raise models.TipoDocumentoSeim.DoesNotExist
        
    print(f"tipo documento seim es {tipo_documento_seim}")
    log_sistema.add_params('tipo_documento_seim', tipo_documento_seim)
    #.info(f'FEA: el documento es {tipo_documento_seim}')
    setLogSistema(log_sistema, f'FEA: el documento es {tipo_documento_seim}', 'INFO', set_log_sistema)

    if models.DocumentoEvaluacionImiv.objects.filter(
        evaluacion_imiv=o_evaluacion,
        tipo_documento_seim=models.TipoDocumentoSeim.get_id(tipo_documento_seim),
        vigente=True
    ).exists():
        print("El documento evaluacion imiv existe")
        #log_sistema.info('El documento evaluacion imiv existe')
        setLogSistema(log_sistema, 'El documento evaluacion imiv existe', 'INFO', set_log_sistema)

        o_documento_evaluacion_imiv = models.DocumentoEvaluacionImiv.objects.get(
            evaluacion_imiv=o_evaluacion,
            tipo_documento_seim=models.TipoDocumentoSeim.get_id(tipo_documento_seim),
            vigente=True
        )
        o_archivo = o_documento_evaluacion_imiv.documento.file

    elif borrador is not None:
        log_sistema.add_params("es_borrador", True)
        o_archivo = borrador.archivo

    else:
        print("No existe documento para enviar a firmar")
        #log_sistema.error("No existe documento para enviar a firmar")
        setLogSistema(log_sistema, "No existe documento para enviar a firmar", 'ERROR', set_log_sistema)
        raise models.DocumentoEvaluacionImiv.DoesNotExist
    
    print("firma_electronica_avanzada: se encontró el documento")
    log_sistema.add_params("o_archivo", o_archivo)
    #.info('firma_electronica_avanzada: se encontró el documento')
    setLogSistema(log_sistema, 'firma_electronica_avanzada: se encontró el documento', 'INFO', set_log_sistema)

    # Distribución externa
    l_distribucion_externa = set([])

    # Interesado
    if o_ficha.tipo_ficha == constants.TIPO_FICHA_SIMPLE:
        o_proyecto_ficha = models.Proyecto_Ficha.objects.filter(ficha_id=o_ficha).first()
        print('firma_electronica_avanzada: es proyecto simple')
        #log_sistema.info('firma_electronica_avanzada: es proyecto simple')
        setLogSistema(log_sistema, 'firma_electronica_avanzada: es proyecto simple', 'INFO', set_log_sistema)

    else:
        print('firma_electronica_avanzada: es proyecto conjunto')
        o_proyecto_ficha = models.Proyecto_Ficha.objects.filter(ficha_id=o_ficha, proyecto_principal=True).first()
        #log_sistema.info('firma_electronica_avanzada: es proyecto conjunto')
        setLogSistema(log_sistema, 'firma_electronica_avanzada: es proyecto conjunto', 'INFO', set_log_sistema)

    personas = obtiene_titular_representante_proyecto(o_proyecto_ficha.proyecto_id.rut_pertenece)
    if personas['titular'] is not None:
        print('firma_electronica_avanzada: El titular no es None')
        l_distribucion_externa.add(personas['titular']['nombre_completo'])

    if personas['responsable'] is not None:
        print('firma_electronica_avanzada: El responsable no es None')
        l_distribucion_externa.add(personas['responsable']['nombre_completo'])

    # AOC
    for aoc in models.Analista_Competente_Ficha.objects.filter(evaluacion_imiv=o_evaluacion).exclude(usuario_respuesta=None):
        print(f'firma_electronica_avanzada: Se añade el AOC {aoc} a la lista de distribución')
        l_distribucion_externa.add(aoc.usuario_respuesta.nombre_completo)

    # AOE
    o_analista_asignado = models.Analista_Asignado.objects.filter(evaluacion_imiv=o_evaluacion, vigente=True).first()
    print(f'firma_electronica_avanzada: Se añade el AOE {o_analista_asignado} a la lista de distribución y la cadena de confianza')
    l_distribucion_externa.add(o_analista_asignado.usuario.nombre_completo)
    l_cadena_confianza_seim = o_analista_asignado.usuario.cadena_de_confianza

    # revisor
    # Solo seremi
    revisor = models.Permiso.objects.filter(
        acceso_id=constants.ACCESO_SEREMITT_SEREMI,
        region_asignada=o_evaluacion.imiv.region_evaluador,
        usuario__estado=True,
        estado=True
    ).first()

    if models.Comuna.objects.filter(provincia__region=o_evaluacion.imiv.region_evaluador, es_capital_regional=True).exists():
        
        l_ciudad = models.Comuna.objects.filter(
            provincia__region=o_evaluacion.imiv.region_evaluador, es_capital_regional=True
        ).first().nombre
    else:
        l_ciudad = ""

    l_organizacion_seim = revisor.region_asignada.nombre_formal.upper()
    l_tipo_materia = 107

    l_distribucion_externa.add(revisor.usuario.nombre_completo)

    l_distribucion_externa.add("Biblioteca")
    l_distribucion_externa.add("Gobierno Transparente")
    l_distribucion_externa_str = ' \n'.join(str(e) for e in l_distribucion_externa)

    l_emisor = settings.EMISOR_DOCUMENTO_EXEDOC

    l_materia = models.TipoDocumentoSeim.get_name(tipo_documento_seim)
    l_id = models.TipoDocumentoSeim.get_id(tipo_documento_seim)
    fechas_plazo = get_fecha_vencimiento_evaluacion(o_evaluacion.id)
    l_plazo_firma = date_to_str_local(fechas_plazo["fecha_plazo_AOE"], "%Y-%m-%d %H:%M:%S")
    l_fecha_tope = date_to_str_local(fechas_plazo["fecha_tope"], "%Y-%m-%d %H:%M:%S")

    l_url_callback = f"{settings.URL_CALLBACK_EXEDOC}{l_id}/{o_archivo.id}/"
    log_sistema.add_params('l_url_callback', l_url_callback)
    #.info(f'FEA: el callback es {l_url_callback}')
    setLogSistema(log_sistema, f'FEA: el callback es {l_url_callback}', 'INFO', set_log_sistema)

    l_nombre_archivo = o_archivo.name

    l_numero_expediente = o_evaluacion.imiv.ficha.expediente
    log_sistema.add_params('l_numero_expediente', l_numero_expediente)
    #.info(f'FEA: el nro de expediente es {l_numero_expediente}')
    setLogSistema(log_sistema, f'FEA: el nro de expediente es {l_numero_expediente}', 'INFO', set_log_sistema)

    l_version_doc = 1
    # TODO  Versión de documento, en un inicio es 1

    responsable = responsable_departamento_exedoc(o_evaluacion.imiv)
    l_firmante = responsable["email"].split("@")[0]

    l_firma_acotada = True if tipo_documento_seim not in [models.TipoDocumentoSeim.RESDES, models.TipoDocumentoSeim.RESNOCOM, models.TipoDocumentoSeim.RESNOCOS] else False

    request_json = {
        "emisor": "seim",
        "documento": {
            "autor": "seim",
            "tipoDocumento": 104,
            "tipoMateria": l_tipo_materia,
            "reservado": False,
            "actosEfectosTerceros": False,
            "antecedentes": "Sin antecedentes",
            "materia": l_materia,
            "emisor": l_emisor,
            "ciudad": l_ciudad,
            "versionDoc": l_version_doc,
            "plazoFirma": l_plazo_firma,
            "firmaAcotada": l_firma_acotada,
            "fechaTope": l_fecha_tope,
            "urlCallbackSeim": l_url_callback,
            "destinatario": ["Expediente IMIV"],
            "dataArchivo": o_archivo.get_url(),
            "nombreArchivo": l_nombre_archivo,
            "contentType": "application/pdf",
            "visadores": [],
            "firmantes": [{
                "usuario": l_firmante,
                "esGrupo": False,
                "orden": "1"
            }],
            "distribucion": [],
            "organizacionSeim": l_organizacion_seim,
            "cadenaConfianzaSeim": l_cadena_confianza_seim,
            "distribucionExterna": l_distribucion_externa_str
        },
        "destinatario": [{
            "usuario": l_firmante,
            "copia": False
        }],
        "observacion": [{
            "texto": "Sin observaciones",
            "adjuntadoPor": "seim"
        }]
    }

    if l_numero_expediente:
        request_json["documento"].update(
            {
                "numeroExpediente": l_numero_expediente
            }
        )

    print('firma_electronica_avanzada: request enviado', request_json)
    log_sistema.add_params('request_json', request_json)
    #.info('FEA: Los parametros de la firma avanzada')
    setLogSistema(log_sistema, 'FEA: Los parametros de la firma avanzada', 'INFO', set_log_sistema)

    o_archivo.request_firma = request_json
    o_archivo.save()

    print(f'firma_electronica_avanzada: call inyectar_doc_exedoc({ficha_id}, {o_archivo}, {log_sistema.to_dict()})')
    return inyectar_doc_exedoc(ficha_id,o_archivo,log_sistema,settings, set_log_sistema)



def inyectar_doc_exedoc(
    ficha_id: str, # id de la ficha
    o_archivo,  # objeto de Archivo
    log_params, # objeto de SeimLogSistema
    settings, # objeto de settings
    set_log_sistema # función de set_log_sistema
):
    """
    Realiza la llamada de GDMTT/EXEDOC.

    
    Argumentos
    ----------
    - ``ficha_id`` (str) : str  id de la ficha
    - ``o_archivo`` (Archivo) :  objeto de Archivo
    - ``log_params`` (SeimLogSistema) : objeto de SeimLogSistema
    - ``settings`` : objeto de settings
    - ``set_log_sistema`` (function) función de set_log_sistema para escribir en el log del sistema

    
    Info
    ----
    - el argumento ``set_log_sistema`` se debe importar de la siguiente manera (ejemplo):
        from polls.services.set_log_sistema import set_log_sistema


           
    Retorno
    -------
    - ``data`` (dict) : diccionario con la respuesta de la llamada a EXEDOC
    - ``status`` (int) : el estado de la respuesta
    - ``URL_GDMTT`` (str|None) : la url de la llamada a EXEDOC
    """
    status = statusClass()
    log_params \
        .add_params("ficha_id", ficha_id) \
        .add_params("request_firma", o_archivo.request_firma)
        #.info("Se inicia la llamada a EXEDOC, en inyectar_doc_exedoc()")

    setLogSistema(log_params, "Se inicia la llamada a EXEDOC, en inyectar_doc_exedoc()", 'INFO', set_log_sistema)
    
    try:
        print("-----------")
        print("Entre al try de firma electronica avanzada")
        response_firma = requests.post(settings.URL_FIRMA_EXEDOC, json=o_archivo.request_firma)
        print(f"El url que se esta usando es {settings.URL_FIRMA_EXEDOC}")
        print("---------")
        log_params \
            .add_params('url', settings.URL_FIRMA_EXEDOC) \
            #.info("Vuelve de EXEDOC, en inyectar_doc_exedoc()")
        setLogSistema(log_params, "Vuelve de EXEDOC, en inyectar_doc_exedoc()", 'INFO', set_log_sistema)

        print("Arme los params de log de firma electrónica avanzada y escribi un log")
        if response_firma.status_code == 200:
            #print("Estoy en el if de resultado = 200")
            response_request = json.loads(response_firma.text)
            log_params \
                .add_params("response_request", response_request) \
                .add_params("data", response_request) \
                .add_params("status", response_firma.status_code) \
                .add_params("URL_GDMTT", settings.URL_FIRMA_EXEDOC)
            #log_params.info("Se guarda el archivo recibido y retornan respuesta")

            setLogSistema(log_params, "Se guarda el archivo recibido y retornan respuesta", 'INFO', set_log_sistema)
            return {
                "data": response_request,
                "status": response_firma.status_code,
                "URL_GDMTT": settings.URL_FIRMA_EXEDOC
            }
        else:
            print("Ocurrió un envío con error a exedoc")
            log_params \
                .add_params("response_firma", response_firma) \
                .add_params("response_firma.status_code", response_firma.status_code) \
                #.warning('Envío con error a EXEDOC')

            setLogSistema(log_params, "Envío con error a EXEDOC", 'WARNING', set_log_sistema)

            if response_firma.status_code == 404:
                print("Estpy en error 404")
                mensaje = "No pudo firmar"
                #log_params.info(f"{mensaje}, error {status.HTTP_404_NOT_FOUND}")
                setLogSistema(log_params, f"{mensaje}, error {status.HTTP_404_NOT_FOUND}", 'INFO', set_log_sistema)
                return {
                    "data": mensaje,
                    "status": status.HTTP_404_NOT_FOUND
                }
            elif response_firma.status_code == 500:
                print("Estoy en error 500")
                mensaje = "Falló la firma"
                #log_params.info(f"{mensaje}, error {status.HTTP_500_INTERNAL_SERVER_ERROR}")
                setLogSistema(log_params, f"{mensaje}, error {status.HTTP_500_INTERNAL_SERVER_ERROR}", 'INFO', set_log_sistema)
                return {
                    "data": mensaje,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            elif response_firma.status_code > 400:
                mensaje = "Falló la firma"
                #log_params.info(f"{mensaje},error {status.HTTP_500_INTERNAL_SERVER_ERROR}")
                setLogSistema(log_params, f"{mensaje}, error {status.HTTP_500_INTERNAL_SERVER_ERROR}", 'INFO', set_log_sistema)
                return { 
                    "data": mensaje,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }
    except Exception as exception:
        log = f'Se produjo intentar firmar documento de ficha: {ficha_id}'
        log_params \
            .add_params('exception', exception.__str__()) \
            .add_params('mensaje', log) \
            .set_traceback('\n '.join(traceback.format_exc().splitlines()), ''.join(traceback.format_stack())) \
            #.error(f'Fallo no controlado en la llamada de exedoc, se devuelve un error {status.HTTP_400_BAD_REQUEST}')
        
        setLogSistema(log_params, f'Fallo no controlado en la llamada de exedoc, se devuelve un error {status.HTTP_400_BAD_REQUEST}', 'ERROR', set_log_sistema)
        return {
            "status": status.HTTP_400_BAD_REQUEST,
            "data": log,
        }
