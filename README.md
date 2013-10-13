Ryepdx's API
===

A personal API implemented in Flask. Provides a layer of abstraction around ryepdx's services.

Please note that I'm approaching this as an experiment. In no way should you expect my personal API to stay static for very long, nor should you ever expect it to be pretty or elegant. I reserve the right to change endpoints all willy-nilly, especially during caffeine-fueled bouts of excitement and tomfoolery.

With that said, every endpoint has a human-readable representation and a machine-readable representation. Human-readable representations can be requested by affixing .html to an endpoint name and machine-readable representations can be requested by affixing .json.

If you think this experiment sounds like loads of fun, feel free to fork and run your own version.

The version in this repository will soon be accessable at the http://ryepdx.com/api endpoint.

I'm also using this as the testing grounds for a small Flask module wrapper that enforces closer matching between browser URL paths and Python module paths, while also encouraging every endpoint to have a machine and a human representation. I call it Cyborg, at least for now, since the idea is to provide a tighter fit between human-consumable and machine-consumable representations of endpoint data. I also suspect it might make it easier to integrate client-side routing with server-side routing, since every endpoint *should* have a machine representation.

One thing to be careful of in Cyborg: any variable or function named "human" or "machine" inside of any variable or function or module named after a particular HTTP method will be accessible. Cyborg allows for dynamic importing of values from wrapped modules. It also allows \_\_getattr\_\_ to be defined on any wrapped module, which allows you to use the "routing by module path" paradigm to generate or retrieve data dynamically based on arbitrary route parameters.

Maybe someday Cyborg will have a proper page and repository of its own, but for now it's just a project I'm working on for fun.
