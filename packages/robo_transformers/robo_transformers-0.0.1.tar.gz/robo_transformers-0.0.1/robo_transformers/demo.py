import os
import sys
from importlib.resources import files

import numpy as np
import PIL.Image as Image
import tensorflow as tf
from absl import app, flags, logging

from robo_transformers.interface import Agent
from robo_transformers.registry import REGISTRY

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "demo_instruction", "pick up the block", "The instruction to run inference on.",
)
flags.DEFINE_string(
    "model_path",
    "rt1x",
    "Which model to load. Can be [rt1main, rt1x, octo-small, octo-base]",
)


flags.DEFINE_boolean("show_images", False, "Whether or not to show the demo images.")

def get_demo_images(output=None) -> np.ndarray:
    """Loads a demo video from the directory.

    Returns:
        list[]: A list of tensors of shape (batch_size, HEIGHT, WIDTH, 3).
    """
    # Suppress noisy PIL warnings.
    log_level = logging.get_verbosity()
    if logging.get_verbosity() < 2:
        logging.set_verbosity(logging.ERROR)

    filenames = [
        files("robo_transformers").joinpath("demo_imgs/gripper_far_from_grasp.png"),
        files("robo_transformers").joinpath("demo_imgs/gripper_mid_to_grasp.png"),
        files("robo_transformers").joinpath("demo_imgs/gripper_almost_grasp.png"),
    ]

    images = []
    for fn in filenames:
        img = Image.open(fn)
        if FLAGS.show_images and output is not None:
            img.save(os.path.join(output, fn.name))
        img = np.array(img.convert("RGB"))
        images.append(img)
    logging.set_verbosity(log_level)
    return images


def run_demo(agent: Agent) -> list:
    # Pass in an instruction through the --demo_instruction flag.
    actions = []
    images = get_demo_images(output=os.getcwd())
    for step in range(3):
        action = agent.act(
            FLAGS.demo_instruction,
            images[step],
        )
        actions.append(action)
    return actions


def main(_) -> None:
    if logging.level_debug():
        tf.debugging.experimental.enable_dump_debug_info(
            "./runs", tensor_debug_mode="FULL_HEALTH", circular_buffer_size=-1,
        )

    # Run three time steps of inference using the demo images.
    # Pass in an instruction via the command line.
    if 'octo' in FLAGS.model_path:
        agent: Agent = REGISTRY['hf']['rail-berkley'](FLAGS.model_path)
    else:
        agent: Agent = REGISTRY['gs']['rt1'](FLAGS.model_path)
    run_demo(agent)


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        pass
    app.run(main)
else:
    # TODO (speralta): Consider reading in flags from argv
    # CAREFUL: This will crash if you allow flags from argv that haven't been
    # defined.
    # For now, only apps that use app.run() can set flags.
    # Read in the program name
    FLAGS(sys.argv[0:1])

