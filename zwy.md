
# 要将proxy写进 bashrc，才可以在ssh上login huggingface
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.bashrc
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.bashrc
source ~/.bashrc

# 在终端设置PYTHONPATH,识别本地路径下的自写库
export PYTHONPATH="/home/kc/workspace/lerobot_pi0_zwy/lerobot:$PYTHONPATH"

# 查看磁盘占用
du -h --max-depth=1 ./ | sort -hr
# 解压缩命令
zstd -dc 014000.tar.zst | tar -xvf -  

# tele示教 因为configs.py里面改了port名，所以需要运行下面.sh进行端口映射
bash run_create_udev_rule.sh

# camera
python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_camera

# 数据采集
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Grasp the colored block, Place it on the black dot, and then return the arm to the default position." \
  --control.repo_id=${HF_USER}/so100_421_pick \
  --control.tags='["so100","tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=30 \
  --control.reset_time_s=30 \
  --control.num_episodes=60 \
  --control.push_to_hub=true \
  --control.resume=true

# 可视化数据
python lerobot/scripts/visualize_dataset_html.py --repo-id ${HF_USER}/so100_321_pick --port 9091

# 训练
python lerobot/scripts/train.py \
  --dataset.repo_id=${HF_USER}/so100_421_pick \
  --policy.type=diffusion \
  --steps=50_000 \
  --save_freq=1_000 \
  --batch_size=10 \
  --output_dir=outputs/so100_421_pick \
  --job_name=so100_421_pick \
  --policy.device=cuda \
  --wandb.enable=true

# 部署
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=50 \
  --control.single_task="Pick the cube." \
  --control.repo_id=./eval_pi0_421_pick_2 \
  --control.tags='["tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=60 \
  --control.reset_time_s=5 \
  --control.num_episodes=10 \
  --control.push_to_hub=false \
  --control.policy.path=outputs/weiye/029000/pretrained_model
