Example implementations with render providers.

# RenderProvider
The RenderProvider handles submitting and tracking jobs as well as uploading/download files.
For job submissions, it receives RenderAppJob instances which are expected to contain all required
arguments for job submission.

# Supported Apps
Any apps intended to be used should first be setup globally (non-provider specific) as an 
AppRenderJob subclass instance which contains all of the arguments required to render a job 
for a particular app type. AppRenderJob is provider agnostic and should contain ALL required information so
that it can be passed to ANY provider for rendering. 

To register an app as valid for a particular provider, create an 'app_handler' entry on the render provider.
The 'app_handler' key is the app_name and the value is a class instance containing any methods to be used
by the render provider. 

Generally, the app handlers are only used for submission since job-tracking/uploding/downloading is usually 
app-agnositic

# App Handlers
When the RenderProvider receives an AppRenderJob instance, it fetches the appropriate app_handler 
based on the AppRenderJob's app_type property.
Specific implementation details for the app_handlers depends entirely on the provider and can be implemented
as you see fit.

