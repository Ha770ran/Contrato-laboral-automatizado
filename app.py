
#importar necesarias para el programa
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer



#Datos SQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contracts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Datos declarados SQL
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(20), nullable=False)
    contract_date = db.Column(db.String(10), nullable=False)
    employer_name = db.Column(db.String(100), nullable=False)
    employer_nit = db.Column(db.String(20), nullable=False)
    legal_representative = db.Column(db.String(100), nullable=False)
    legal_representative_id = db.Column(db.String(20), nullable=False)
    employer_address = db.Column(db.String(200), nullable=False)
    worker_name = db.Column(db.String(100), nullable=False)
    worker_id = db.Column(db.String(20), nullable=False)
    worker_city = db.Column(db.String(100), nullable=False)
    worker_address = db.Column(db.String(200), nullable=False)
    worker_phone = db.Column(db.String(20), nullable=False)
    worker_email = db.Column(db.String(100), nullable=False)
    worker_birthdate = db.Column(db.String(10), nullable=False)
    worker_birthplace = db.Column(db.String(100), nullable=False)
    worker_position = db.Column(db.String(100), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_city = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(20), nullable=False)
    payment_frequency = db.Column(db.String(20), nullable=False)
    contract_start_date = db.Column(db.String(10), nullable=False)
    contract_duration_percentage = db.Column(db.String(5), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)

#from app import app, db  # Asegúrate de importar tu aplicación y la instancia de SQLAlchemy#(no tener en cuenta)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    new_contract = Contract(
        contract_number=request.form['contract_number'],
        contract_date=request.form['contract_date'],
        employer_name=request.form['employer_name'],
        employer_nit=request.form['employer_nit'],
        legal_representative=request.form['legal_representative'],
        legal_representative_id=request.form['legal_representative_id'],
        employer_address=request.form['employer_address'],
        worker_name=request.form['worker_name'],
        worker_id=request.form['worker_id'],
        worker_city=request.form['worker_city'],
        worker_address=request.form['worker_address'],
        worker_phone=request.form['worker_phone'],
        worker_email=request.form['worker_email'],
        worker_birthdate=request.form['worker_birthdate'],
        worker_birthplace=request.form['worker_birthplace'],
        worker_position=request.form['worker_position'],
        project_name=request.form['project_name'],
        project_city=request.form['project_city'],
        salary=request.form['salary'],
        payment_frequency=request.form['payment_frequency'],
        contract_start_date=request.form['contract_start_date'],
        contract_duration_percentage=request.form['contract_duration_percentage'],
        emergency_contact_name=request.form['emergency_contact_name'],
        emergency_contact_phone=request.form['emergency_contact_phone']
    )
    db.session.add(new_contract)
    db.session.commit()

    generate_pdf(new_contract)

    return redirect(url_for('index'))

    # Aquí es donde defines los elementos del documento.
    elements = []

#generar el contrato:
def generate_pdf(contract):
    pdf_filename = f"{contract.contract_number}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    page_number = 1

     # Título centrado
    title = "CONTRATO INDIVIDUAL DE TRABAJO POR OBRA O LABOR"
    c.setFont("Helvetica-Bold", 16)
    title_y = 720 # Ajuste la coordenada Y para acercar el título
    c.drawCentredString(letter[0] / 2.0, title_y, title.upper())

    # Ajuste de espacio entre el título y el cuadro de variables
    space_between_title_and_table = 10  # Espacio equivalente a 5 líneas
    table_start_y = title_y - space_between_title_and_table - 20

    # Datos organizados en un array bidimensional
    data = [
        ["Número de Contrato:", contract.contract_number],
        ["Fecha del Contrato:", contract.contract_date],
        ["Nombre del Empleador:", contract.employer_name],
        ["Empleador NIT:", contract.employer_nit],
        ["Nombre Representante Legal:", contract.legal_representative],
        ["Representante Legal Numero CC:", contract.legal_representative_id],
        ["Dirección del Empleador:", contract.employer_address],
        ["Nombre del Trabajador:", contract.worker_name],
        ["CC del Trabajador:", contract.worker_id],
        ["Ciudad donde reside el trabajador:", contract.worker_city],
        ["Dirección del trabajador:", contract.worker_address],
        ["Numero celular del trabajador:", contract.worker_phone],
        ["Correo electronico del trabajador:", contract.worker_email],
        ["Fecha nacimiento del Trabajador:", contract.worker_birthdate],
        ["Lugar nacimiento del Trabajador:", contract.worker_birthplace],
        ["Cargo del Trabajador:", contract.worker_position],
        ["Nombre del Proyecto o Area:", contract.project_name],
        ["Ciudad donde ejecutara la labor:", contract.project_city],
        ["Salario:", contract.salary],
        ["Frecuencia de pago:", contract.payment_frequency],
        ["Fecha de inicio:", contract.contract_start_date],
        ["Porcentaje de duración del contrato:", contract.contract_duration_percentage],
        ["Contacto de emergencia:", contract.emergency_contact_name],
        ["Numero del contacto de emergencia:", contract.emergency_contact_phone],
    ]

    # Crear tabla
    table = Table(data, colWidths=[2.5 * inch, 3 * inch])

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.mediumslateblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.floralwhite),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    

    # Calcular el ancho y alto de la tabla
    table_width, table_height = table.wrap(0, 0)

    # Calcular las coordenadas x, y para centrar la tabla en la página
    x_position = (letter[0] - table_width) / 2
    y_position = table_start_y - table_height

    # Dibujar la tabla en el PDF centrada
    table.drawOn(c, x_position, y_position)

    # Añadir espacio entre la tabla y el texto
    additional_spacing = 50  # Espacio adicional (equivalente a 2 líneas)
    paragraph_y_position = y_position - additional_spacing

    new_y_position = y_position - 20  # Ajusta el espaciado según sea necesario

    # Crear el estilo para el párrafo
    styles = getSampleStyleSheet()
    paragraph_style = styles['BodyText']
    paragraph_style.alignment = 4  # Justificación completa

    # Texto del párrafo
    additional_text = (
    "Las partes identificadas pplenamente en el presente contrato laboral deciden de "
    "mutuo acuerdo, libre y voluntariamente, pactar y cumplir las siguientes condiciones" 
    "contractuales, de acuerdo a la normatividad laboral colombiana."
    )

    # Crear el párrafo
    paragraph = Paragraph(additional_text, paragraph_style)

    # Ajustar la posición del párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, paragraph_y_position)

    # Insertar el número de página al pie
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    # Finalizar la primera página
    c.showPage()

    # Incrementar el número de página
    page_number += 1

    # Determinar la forma y presentación para los parrafos de las páginas adicionales que estan en las paginas 1,2,3
    styles = getSampleStyleSheet()
    paragraph_style = styles['BodyText']
    paragraph_style.alignment = 4  # Justificación completa

    additional_text_1 = (
        "Entre el EMPLEADOR y el TRABAJADOR, de las condiciones ya dichas, identificados como " 
        "aparecen al pie de sus firmas, se ha celebrado el presente contrato individual de trabajo por "
        "duración de la obra o labor contratada, regido además por las siguientes cláusulas:\n\n"

        "<b>PRIMERA</b>: El TRABAJADOR se compromete a colocar al servicio del empleador toda su capacidad "
        "normal de trabajo, en forma exclusiva y personal, en el desempeño de las funciones que se le "
        "asignen, y especialmente las relacionadas con el cargo y en las labores anexas y "
        "complementarias del mismo, de conformidad con las leyes, los reglamentos, las órdenes y las "
        "instrucciones generales o particulares que se le impartan, observando en su desempeño la "
        "buena fe, el cuidado y diligencia necesarios, durante el tiempo que para su especialidad de "
        "trabajo lo requiera la ejecución de la obra ya mencionada, la cual terminada automáticamente "
        "dará por terminado el presente contrato.\n\n"

        "<b>SEGUNDA</b>: DURACIÓN DEL CONTRATO. El presente contrato se celebra por el tiempo que dure la "
        "realización de la obra o labor contratada, de acuerdo con las condiciones generales que se "
        "señalan al inicio del presente contrato.\n\n"

        "<b>TERCERA</b>: PERÍODO DE PRUEBA. - El presente contrato queda sujeto a un período de prueba "
        "equivalente a la quinta parte de duración del presente contrato, sin que sea superior a dos 2"
        "(dos) meses contados a partir de la fecha de la iniciación de la relación laboral, plazo "
        "durante el cual cualquiera de las partes podrá darlo por terminado unilateralmente sin previo "
        "aviso y sin lugar al pago de indemnización. Si vencido el período de prueba EL TRABAJADOR "
        "continuare prestando sus servicios con la aceptación expresa o tácita de EL EMPLEADOR, la "
        "duración del contrato será por el tiempo que dure la realización de la obra o labor contratada, "
        "mientras subsistan las causas que le dieron origen y la materia del trabajo.\n\n"

        "<b>CUARTA</b>: EL TRABAJADOR laborará durante las horas diarias que como jornada ordinaria le señale EL "
        "EMPLEADOR de acuerdo con el Reglamento Interno de Trabajo, sin exceder las horas semanales "
        "establecidas en la Ley 2101 de 2021 que este aplicando el EMPLEADOR, en cualquiera de los turnos "
        "u horarios correspondientes a su oficio y además durante el tiempo extraordinario que LA EMPRESA "
        "le exija de acuerdo con la Ley. La labor en tiempo suplementario, siempre que le haya sido "
        "previamente autorizado por LA EMPRESA, le será cubierta a la tarifa legal. Por el acuerdo expreso "
        "o tácito de las partes, podrá repartirse las horas de la jornada ordinaria en la forma prevista en "
        "el Art. 164 del C.S.T., modificado por el Artículo 23 de la Ley 50/90, teniendo en cuenta que los "
        "tiempos de descanso entre las secciones de la jornada no se computan dentro de la misma, según el "
        "Artículo 167 ibídem.\n\n"

        "<b>QUINTA</b>: EL EMPLEADOR reconocerá al empleado los viáticos accidentales y los gastos de representación, "
        "que se puedan generar y sea previamente acordado por las partes mediante documento escrito que deberá "
        "estar adicionado al presente contrato.\n\n"

        "<b>SEXTA</b>: EL TRABAJADOR prestará sus servicios durante todos los días laborables de cada semana y "
        "descansará el domingo; pero si por razón de su oficio debe trabajar habitualmente en domingos, tomará "
        "un día de descanso compensatorio por cada semana completa de labor, en uno cualquiera de los días "
        "laborables de la semana siguiente.\n\n"

        "<b>SEPTIMA</b>: OBLIGACIONES DE EL TRABAJADOR. El trabajador se obliga a:\n\n"
            "1.	A no atender durante las horas de trabajo ocupaciones o asuntos diferentes a los que le encomiende "
                "EL EMPLEADOR.\n\n"
            "2.	Abstenerse de cualquier actitud en los compromisos comerciales, personales o en las relaciones "
                "sociales, que pueda afectar en forma nociva la reputación del empleador.\n\n"
            "3.	No solicitar préstamos especiales o ayuda económica a los clientes del empleador aprovechándose "
                "de su cargo u oficio o aceptarles donaciones de cualquier clase sin la previa autorización escrita del "
                "empleador.\n\n"
            "4.	No retirar de las instalaciones donde funcione la empresa elementos, máquinas y útiles de propiedad del "
                "empleador sin su autorización escrita.\n\n"
            "5.	No presentar cuentas de gastos ficticias o reportar como cumplidas visitas o tareas no efectuadas.\n\n"
            "6.	No autorizar o ejecutar sin ser de su competencia, operaciones que afecten los intereses del empleador "
                "o negociar bienes y/o mercancías del empleador en provecho propio.\n\n"
            "7.	No retener dinero o hacer efectivos cheques recibidos para el empleador.\n\n"
            "8.	Utilizar adecuadamente los implementos de seguridad que EL EMPLEADOR tenga establecidos como tal.\n\n"
            "9.	A trabajar todo el tiempo que sea necesario para cumplir cabalmente sus deberes.\n\n"
            "10. A prestar sus servicios en cualquier otro empleo, cargo u oficio a donde lo promueva EL EMPLEADOR, "
              "ya sea en la sede inicial del trabajo o en cualquier otra, donde desarrolle su objeto social; dentro de "
              "su poder subordinante, siempre que se respeten las condiciones laborales EL EMPLEADO y no se le causen "
              "perjuicios. Todo ello sin que se afecte el honor, la dignidad y los derechos mínimos de EL EMPLEADO.\n\n"
             "11. A guardar confidencialidad sobre todo a la vinculación laboral y sobre la información a la cual tenga "
               "acceso por el desempeño de sus funciones, so pena de incumplir las obligaciones derivadas del presente "
               "contrato de trabajo, sin perjuicio de que en su contra se adelanten las acciones legales respectivas e " 
               "independientemente de la decisión que adopte EL EMPLEADOR frente a su vinculación laboral.\n\n"
    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_1, paragraph_style)
    
    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 650) 

    # Insertar el número de página al pie (pag 1)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 1 de texto.
    c.showPage()

    # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 2
 
    additional_text_2 = (
            "12. A no ofrecer sus servicios o experiencia profesional a título personal, o los servicios o experiencia "
              "profesional de sus amigos, parientes o sociedades con las cuales tenga alguna vinculación, en competencia "
               "con los servicios o productos que presta o fabrique EL EMPLEADOR.\n\n"
            "13. A no prestar directa e indirectamente sus servicios laborales a otros empleadores, sin autorizaciòn"
            "14. A no utilizar los recursos humanos, físicos, financieros e información en general de EL EMPLEADOR para "
              "beneficio propio o de terceros.\n\n"
            "15. Planear, organizar, dirigir, coordinar, controlar y supervisar el trabajo de cada uno de sus "
              "subalternos con el fin de que se realicen las labores de dentro de las normas de EL EMPLEADOR.\n\n"
            "16. Aplicar las políticas, los reglamentos, las normas y procedimientos de EL EMPLEADOR.\n\n"
            "17. Mantener la disciplina y comunicación dentro del grupo puesto bajo sus órdenes.\n\n"
            "18. Abstenerse de solicitar en préstamo en dinero a sus subalternos o superiores.\n\n"
            "19. Asistir a las capacitaciones a las que sea enviado por EL EMPLEADOR.\n\n"
            "20. Sólo instalar software que cuenten con la debida licencia de uso en los computadores de la empresa "
              "o en uno de su propiedad que se encuentre dentro de las instalaciones de EL EMPLEADOR.\n\n"
            "21. No instalar software en los computadores de EL EMPLEADOR así cuenten con la licencia otorgada por "
             "el fabricante en los términos de ley, sin autorización expresa.\n\n"
            "22. Sólo utilizar la red de Internet dispuesta por EL EMPLEADOR para los fines propios del desempeño de su "
             "cargo, incluida la utilización de la cuenta de correo electrónico dispuesta por EL EMPLEADOR para el "
             "ejercicio de sus funciones.\n\n"
            "23. No dar a conocer a personas no autorizadas la clave personal de acceso a los sistemas de cómputo de EL "
             "EMPLEADOR, ni utilizar las claves de acceso de otros empleados.\n\n"
            "24. No ingresar equipos de cómputo a las instalaciones de EL EMPLEADOR sin autorización expresa.\n\n"
        "<b>PARÁGRAFO</b>: - Las faltas anteriormente indicadas no son taxativas dentro de los motivos de despido con justa "
        "causa, pues también tendrán aplicación para tal fin las que se desprendan de las normas legales.\n\n"

        "<b>OCTAVA</b>: Al TRABAJADOR se le aplicara los derechos y deberes establecidos en el CST Colombiano.\n\n"

        "<b>NOVENA</b>: Los dineros que el TRABAJADOR reciba ocasionalmente o en forma habitual, o por mera liberalidad, "
        "por concepto de primas, alimentación, viáticos, bonificación por las tareas, participación de utilidades "
        "no constituirán salario, ni se computarán como factor salarial de acuerdo a los artículos 15 y 16 de la "
        "Ley 50/90, ya que se entiende que dichos pagos son un medio para facilitar la prestación del servicio y "
        "para desempeñar a cabalidad las funciones.\n\n"

        "<b>PARÁGRAFO PRIMERO</b>:- Las partes acuerdan que ninguno de los pagos enumerados en el artículo 128 del C. S. T. "
        "subrogado por el artículo 15 de la Ley 50/90, tiene carácter de salario, incluidos aquellos pagos que se "
        "hagan por concepto de alimentación, vestuario y/o gasolina y demás con base en vales canasta para compra de "
        "productos en supermercados u otros establecimientos, aquellas que ocasionalmente y por mera liberalidad "
        "reciba el TRABAJADOR de EL EMPLEADOR como bonificaciones, gratificaciones ocasionales, y el general todo "
        "aquello que reciba en dinero o en especie, que no sea para su beneficio, ni para enriquecer su patrimonio, "
        "sino para desempeñar a cabalidad sus funciones tales como gastos de representación, ropa de trabajo, dotación, "
        "transporte, elementos de trabajo, alimentación que le vende EL EMPLEADOR a bajo precio, los servicios y "
        "auxilios que reciban sus familiares tales como servicios médicos, auxilios para drogas, becas, auxilio de fondo "
        "quirúrgico, auxilio de escolaridad, y en general, cualquier servicio o beneficio que reciba él o sus familiares.\n\n"

        "También convienen expresamente las partes que de conformidad con la misma norma, no constituyen factor salarial " 
        "para efectos de liquidación de prestaciones sociales, reconocimiento de indemnizaciones, ni para ningún otro " 
        "efecto, los gastos de transporte, gastos de viaje y las sumas destinadas a manutención y alojamiento cuando " 
        "EL TRABAJADOR deba desplazarse de su sede habitual de trabajo, los gastos sufragados con tarjetas de crédito "
        "empresariales, acciones, cuotas de sostenimiento y consumos de clubes sociales, gastos de relaciones públicas, las " 
        "primas de los seguros de vida, accidentes, cirugía y hospitalización, etc. canceladas por EL EMPLEADOR en beneficio "
        "de los TRABAJADORES reconocidas en dinero o en especie, ni los demás beneficios o auxilios habituales u ocasionales "
        "que en forma extralegal llegue a conceder EL EMPLEADOR a sus trabajadores incluidas las bonificaciones por "
        "incremento en las operaciones. Así mismo, también se deja expresa constancia de que el cargo que desempeñará EL"
        "TRABAJADOR no genera viáticos permanentes que puedan constituir salario.\n\n"
 
        "<b>PARAGRAFO SEGUNDO</b>: Los gastos de telefonía celular o de cualquier otro medio de comunicación, los gastos de transporte, " 
        "los gastos de viaje y las sumas destinadas a manutención y alojamiento de El TRABAJADOR cuando deba desplazarse de su "
        "sede habitual de trabajo, y que sean cancelados por EL EMPLEADOR no constituirán salario toda vez que los mismos no "
        "tienen por efecto remunerar la prestación del servicio sino disponer los medios necesarios para que este pueda prestarse.\n\n"

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_2, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 650) 

     # Insertar el número de página al pie (pag 2)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 2 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 3
 
    additional_text_3 = (
       "<b>DÉCIMA</b>: EL TRABAJADOR autoriza expresamente a EL EMPLEADOR para que, al finalizar este contrato por cualquier causa, "
        "deduzca y compense de las sumas que le correspondan por concepto de salarios, prestaciones e indemnizaciones de "
        "carácter laboral, las cantidades y saldos pendientes a su cargo y a favor de ella, por razón de préstamos personales "
        "o de vivienda, valor de facturas por suministro de drogas, víveres o mercancías que haya recibido a crédito, o por "
        "cualquiera otra causa.\n\n"

        "<b>DÉCIMA PRIMERA</b>: Hace parte de este contrato el reglamento interno del trabajo, manual de funciones y procesos "
        "establecidos para el cargo.\n\n"

        "<b>DÉCIMA SEGUNDA</b>: El TRABAJADOR (a) declara expresamente que fue notificado y acepta que la dirección y número "
        "telefónico suministrados por el (ella) en el presente contrato de trabajo es su domicilio y residencia principal "
        "y que allí se le puede enviar cualquier correspondencia que fuere necesaria, que en caso de traslado de dirección "
        "informará por escrito dentro de los cinco (5) primeros días hábiles a la fecha en que se produzca su traslado.\n\n"

        "<b>DÉCIMA TERCERA</b>: En virtud de lo dispuesto en la Ley 1581 de 2012 y demás normas concordantes, el trabajador "
        "autoriza de manera libre, expresa y voluntaria al empleador para que realice el tratamiento de sus datos " 
        "personales, los cuales serán utilizados exclusivamente para fines relacionados con la gestión laboral de " 
        "la compañía. El trabajador declara que ha sido informado sobre los derechos que le asisten en calidad de "
        "titular de los datos, así como de las finalidades del tratamiento. Asimismo, exonera al empleador de toda " 
        "responsabilidad por el uso de los datos personales siempre que este uso se realice dentro del marco de "
        "las relaciones laborales. "
        
        "<b>DECIMA CUARTA</b>: El presente contrato reemplaza en su integridad y deja sin efecto cualquiera otro contrato verbal "
        "o escrito celebrado entre las partes con anterioridad. Las modificaciones que se acuerden al presente contrato se " 
        "anotarán a continuación de su texto.\n\n"

        "<b>DÉCIMA QUINTA</b>: Las modificaciones al presente contrato podrán elaborarse en una hoja anexa a este documento, la "
        "cual hará parte del mismo y donde deberán consignarse los nombres y firmas de las partes contratantes, su documento "
        "de identidad y fecha en que se efectué la modificación.\n\n"

        "<b>DÉCIMA SEXTA</b>: Este contrato ha sido redactado estrictamente de acuerdo con la Ley y la Jurisprudencia y será "
        "interpretado de buena fe y en consonancia con el C.S.T., cuyo objeto, definido en su Artículo 1º, es lograr en las "
        "relaciones entre EL EMPLEADOR y LOS TRABAJADORES dentro de un espíritu de coordinación económica y equilibrio social.\n\n"

        "El presente contrato ha sido discutido libremente por las partes, las cuales aprueban todas las estipulaciones que lo "
        "conforman y en consecuencia para constancia se firma en dos o más ejemplares del mismo tenor y valor, ante testigos, "
        "un ejemplar de los cuales recibe EL TRABAJADOR en este acto.\n\n"
    
    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_3, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 400) 

    # Añadir espacio antes de la sección de firmas
    c.drawString(50, letter[1] - 700, "")  # Solo para establecer la coordenada, ajusta si es necesario.
    c.drawString(50, letter[1] - 680, "FIRMA DEL EMPLEADOR                 FIRMA Y CEDULA DEL TRABAJADOR")

    # Añadir espacio después del texto
    c.drawString(50, letter[1] - 720, "_____________________                 ____________________________")

     # Insertar el número de página al pie (pag 3)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 3 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    additional_text_4 = (

        "                                <b>ANEXO 1 AL CONTRATO DE TRABAJO</b>\n\n"

        "ASUNTO: REQUISITOS PARA SU VINCULACIÓN AL SISTEMA DE SEGURIDAD SOCIAL" 
        "COTIZANTE Y BENEFICIARIOS (ARP, EPS, AFP, CCF).\n\n"

        "1.	 Tres (3) fotocopias ampliadas legibles de la cedula de ciudadanía. "
        "2.	 Certificado de afiliación EPS a la que pertenece. "
        "3.	 Certificado de Fondo de pensión al que pertenece. "
        "4.	 Tres (3) fotocopias de la cedula del cónyuge o compañero (a) permanente. "
        "5.	 Dos (2) certificados de matrimonio registrado ante notaria o declaración extra juicio (si no existe matrimonio legal, "
        "con una vigencia no mayor a tres (3) meses). "
        "6.	 Dos (2) registros civiles de cada uno de los hijos: estos registros deben tener NUIP y para mayores de 10 años se debe "
        "enviar también la tarjeta de identidad, sino la sacan en la región enviar certificado donde conste esto. "
        "7.	 Un (1) certificado de estudio original para cada uno de los hijos mayores de 12 años. "
        "8.	 Cuando los hijos son mayores de 18 años es necesario: 2 certificados de estudio originales, 2 registros civiles, " 
        "dos (2) fotocopias de la cédula (solo para EPS). Recuerde que por ley los hijos mayores de 18 años no reciben cuota "
        "monetaria de la caja de compensación. "
        "9.	 Para afiliar padres mayores de 60 años: registro civil de nacimiento del Trabajador, fotocopias de cedula de los "
        "padres, certificado de supervivencia y certificado de dependencia económica ante notaria. "
        "10.  Si es soltero puede afiliar a los padres a la EPS y Caja de compensación es necesario: Registro civil de " 
        "nacimiento del trabajador, fotocopias de la cedula de los padres y certificado extra juicio de dependencia " 
        "económica y supervivencia ante notaria.\n\n"
        "Certifico que fui notificado de estos requisitos, por lo tanto, es mi responsabilidad presentar dicha " 
        "documentación y en caso de no hacerlo, mi empleador queda exonerado de cualquier reclamación.\n\n"

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_4, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 300) 

    #Adicionar parrafo 5 a la misma pagina 4
    additional_text_5 = ( "<b>DECLARACIÓN JURAMENTADA DEL TRABAJADOR</b>:"
        "El trabajador declara expresamente que asistió a la charla de inducción y Salud Ocupacional donde se le explican:\n\n" 
        "el reglamento interno de trabajo, el reglamento de higiene y seguridad industrial, matriz de riesgos laborales de la "
        "empresa, las normas, procedimientos y cuidados inherentes a su cargo. \n\n"
        "De igual manera declara que recibió por parte de la empresa los elementos de protección personal requeridos para " 
        "desarrollar su cargo y que recibió la capacitación respectiva acerca de su uso. Declara que está obligado a utilizarlos " 
        "y que cualquier accidente de trabajo que ocurra por no utilizarlos correrá por su cuenta y a riesgo propio, en tanto la " 
        "empresa quedará exonerada y no tendrá ninguna responsabilidad.\n\n")

     # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_5, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 450) 

    # Añadir espacio antes de la sección de firmas
    c.drawString(50, letter[1] - 700, "")  # Solo para establecer la coordenada, ajusta si es necesario.
    c.drawString(50, letter[1] - 680, "FIRMA Y CEDULA DEL TRABAJADOR")

    # Añadir espacio después del texto
    c.drawString(50, letter[1] - 720, "____________________________")

     # Insertar el número de página al pie (pag 4)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 4 de texto
    c.showPage()

    #guardad PDF
    c.save()
   
if __name__ == '__main__':
    app.run(debug=True)