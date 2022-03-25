from __future__ import print_function

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.me', 
          'https://www.googleapis.com/auth/classroom.announcements.readonly',
          'https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.courseworkmaterials',
          'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly']

creds = None
today = int(date.today().strftime("%d"))
month = int(date.today().strftime("%m"))
textual_month = date.today().strftime("%B")

# print("Today is: {}. The next weekend is {}, {}".format(today, textual_month, today + 6))

def authenticate_user():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    global creds

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

def list_active_courses():
    try:    
        service = build('classroom', 'v1', credentials=creds)
        result = service.courses().list(courseStates="ACTIVE").execute()
        courses = result.get('courses', [])
        names = []
        for course in courses:
            names.append(course['name'])

        return names
    
        if not courses:
            print('No courses found')
            return

    except HttpError as error:
        print('An error occured: %s' % error)

def get_course_name(courseId):
    try: 
        service = build('classroom', 'v1', credentials=creds)
        course_info = service.courses().get(id=courseId).execute()
        return course_info['name']

    except HttpError as error:
        print('An error occured %s' % error)

def list_courseWork(courseId):
    try:
        service = build('classroom', 'v1', credentials=creds)
        courseWork = service.courses().courseWork().list(courseId=courseId).execute()
        results = courseWork.get('courseWork', [])
        # print(json.dumps(results, indent=4))
        assignments = []
        for i in results:
            tmpAssignment = []
            tmpAssignment.append(i['title'])
            tmpAssignment.append(i['id'])
            tmpAssignment.append(i['dueDate'])
            #tmpAssignment.append(i['description'])
            assignments.append(tmpAssignment)
        return assignments

    except HttpError as error:
            print('An error occurred: %s' % error)

def list_upcoming_assignments(courseId):
    try:
        service = build('classroom', 'v1', credentials=creds)
        assigments = []
        course_name = get_course_name(courseId)
        # print('{} assignments for the next week:'.format(course_name))


        for course in courses:
            tareas = service.courses().courseWork().list(courseId=course.get('id'), orderBy="dueDate desc").execute()
            publicadas = tareas.get('courseWork', [])
            print(json.dumps(publicadas, indent=4))
            '''dueDate = .get('dueDate')
            print("Tareas para {} \t {}".format(course.get('name'), course.get('id')))
            if dueDate is not None:
                if dueDate['day'] in range (today, today + 6) and dueDate['month'] >= month:
                    state = tarea.get('state')
                    if state != 'RETURNED' or 'TURNED_IN':
                        for tarea in publicadas:
                            print("\t{} -> {}/{}".format(' '.join(tarea.get('title').split()), dueDate.get('day'), dueDate.get('month') ) )'''




            """for tarea in publicadas:
                state = tarea.get('state')
                if dueDate is not None and dueDate['day' in range (today, today + 6)] and dueDate['month'] >=month and state is not 'RETURNED':
                    if dueDate['day'] in range (today, today + 6) :
                else: 
                    print("\tTarea encontrada sin fecha de entrega")"""

    except HttpError as error:
        print('An error occurred: %s' % error)

def getSubmissionState(courseId, courseWorkId):
    try:
        # Construyendo el servicio para enviar la solicitud
        service = build('classroom', 'v1', credentials=creds)
        # La petición a la API
        submission = service.courses().courseWork().studentSubmissions().list(courseId=courseId, courseWorkId=courseWorkId).execute()
        submission_properties = submission.get('studentSubmissions', [])
        for state in submission_properties:
            return state['state']

    except HttpError as error:
        print('An error occurred: %s' % error)


def main():
    algebraId = '451407366421'
    tareaAlgebra = '457015118004'

    # Authenticate user and set credentials to work ith
    authenticate_user()
    algebra = list_courseWork(algebraId)
    print(algebra[9][0])
    
if __name__ == '__main__':
    main()
    '''Pendientes para la refactorizacion del código
        - Construir el servicio una sola vez, no en cada función
        - Hacer la menor cantidad de llamadas posibles
        
      ¿Qué valores requiere la API de Notion?
        * Base de datos Homework - todo estos valores se pueden obtener con la llamada a la ruta de courseWork.list
            <Propiedades>
            - Nombre de la tarea
            - Materia (id)
            - Fecha de entrega
            <Contenido>
            - Instrucciones
            - Materiales o recursos
        '''
        # Para ver el estado de una tarea entregada o devuleta, por ejemplo
        # la ruta ideal es courses().courseWork().studentSubmissions().list(courseId=, couseWorkId=)

