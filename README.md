# cog-inject - inject files into cog models

This is a proof of concept that:

 - takes an input of files in a zip `weights`
 - where those files should end up on disk `path_base`
 - the name of an image to build ontop of `base_image`
 - and where you want to push `dest_image`

On a CPU, without downloading the `base_image`, this uses a small go binary built on [google/go-containerregistry](https://github.com/google/go-containerregistry) to create a new image layer, and push that layer / image metadata to `dest_image`

## Why?

There are "weights" and there are "models".  Whenever I get new weights (either through dreambooth, AIT, some new model shared on HF/civit/reddit), I want to be able to use them efficiently. 

This builds a new image in around a minute, without any GPU or time spent waiting for cog to build/push.

## Hmm, you send your auth_token?!!?!

yeah, this is a prototype, **do not use in production**

please experiment and share feedback with replicate team in discord