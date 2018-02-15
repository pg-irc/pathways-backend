from drf_yasg import openapi, views
from rest_framework import permissions

def build_schema_view():
    info = openapi.Info(title='Pathways HSDA',
                        default_version='v1',
                        description='PeaceGeeks implementation of OpenReferral Human Services HSDA',
                        #terms_of_service='https://www.google.com/policies/terms/',
                        contact=openapi.Contact(email='rasmus@peacegeeks.org'),
                        license=openapi.License(name='MIT License'),
                       )

    return views.get_schema_view(info,
                                 #validators=['flex', 'ssv'],
                                 public=True,
                                 permission_classes=(permissions.AllowAny,),
                                )
