import io
import os
import shutil
import subprocess
import urllib
import zipfile
import tarfile
import time

from cog import BasePredictor, Input, Path


class Predictor(BasePredictor):
    def download_zip_weights_python(self, url, dest):
        """Download the model weights from the given URL"""
        print("Downloading weights...")
        start = time.time()

        url = url.replace(
            "https://replicate.delivery/pbxt/",
            "https://storage.googleapis.com/replicate-files/",
        )

        if url.endswith(".zip"):
            request = urllib.request.urlopen(url)
            with zipfile.ZipFile(io.BytesIO(request.read())) as zf:
                zf.extractall(dest)
        else:
            print("Unknown file type: {}".format(url))

        print("Downloaded weights in {:.2f}s".format(time.time() - start))

    def make_tarfile(self, output_filename, source_dir, dest_base):
        print("Making tarfile...")
        start = time.time()
        with tarfile.open(output_filename, "w") as tar:
            directory = Path(source_dir)
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    print(file_path)
                    tar.add(
                        file_path,
                        arcname=os.path.join(
                            dest_base, file_path.relative_to(source_dir)
                        ),
                    )

        print("Made tarfile in {:.2f}s".format(time.time() - start))

    def predict(
        self,
        weights: str = Input(description="Input weight zip"),
        auth_token: str = Input(description="your replicate auth token"),
        dest_image: str = Input(description="dest image: r8.im/username/template"),
        base_image: str = Input(description="base image: r8.im/username/new_image"),
        path_base: str = Input(
            description="path base: /src/weights", default="/src/weights"
        ),
    ) -> str:
        weights_tar = "weights.tar"
        if os.path.exists(weights_tar):
            os.remove(weights_tar)

        weights_dir = "weights"
        if os.path.exists(weights_dir):
            shutil.rmtree(weights_dir)

        self.download_zip_weights_python(weights, weights_dir)
        self.make_tarfile(weights_tar, weights_dir, path_base)

        print("pushing image...")
        start = time.time()
        subprocess.check_call(
            [
                "./r8",
                "affix",
                "-t",
                auth_token,
                "-d",
                dest_image,
                "-b",
                base_image,
                "-f",
                weights_tar,
            ],
            stderr=subprocess.STDOUT,
        )
        print("pushed image in {:.2f}s".format(time.time() - start))

        return dest_image
