class SpiderCLIException(Exception):...

class ProjectTypeNotExitsError(SpiderCLIException):

    def __str__(self):
        return f'This project type is not a supported.'
    
class PathCreateError(SpiderCLIException):

    def __str__(self) -> str:
        return 'This path already exists.'
    
class FileCreateError(SpiderCLIException):

    def __str__(self) -> str:
        return 'This file already exists.'
    
class ContinousIntegrationServiceError(SpiderCLIException):
    def __str__(self) -> str:
        return 'This continous integration service is not supported.'
    
class VenvCreateError(SpiderCLIException):
    def __str__(self) -> str:
        return 'An error occurred during create virtual environment process.'
    
class RequirementsInstallationError(SpiderCLIException):
    def __str__(self) -> str:
        return 'An error occurred during installation of requirements process.'
    
class CreateProjectStructureError(SpiderCLIException):
    def __str__(self) -> str:
        return 'An error occurred during project structure creation process.'