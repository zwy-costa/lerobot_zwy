# 局域网文件传输
python -m http.server

# 要将proxy写进 bashrc，才可以在ssh上login huggingface
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.bashrc
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.bashrc
source ~/.bashrc

# 在终端设置PYTHONPATH,识别本地路径下的自写库
export PYTHONPATH="/home/kc/workspace/lerobot_pi0_zwy/lerobot:$PYTHONPATH"

# 查看磁盘占用
du -h --max-depth=1 ./ | sort -hr
# 解压缩命令
zstd -dc 0613_pi0_Deg2Rad_30w.tar.zst | tar -xvf -

# tele示教 因为configs.py里面改了port名，所以需要运行下面.sh进行端口映射
bash run_create_udev_rule.sh

# camera
python lerobot/common/robot_devices/cameras/opencv.py \
    --images-dir outputs/images_from_opencv_camera

# 摇操作
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=teleoperate
  --control.fps=30

# 数据采集
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Grasp the colored block, Place it on the black dot, and then return the arm to the default position." \
  --control.repo_id=weiye11/0613_pi0_Deg2Rad \
  --control.tags='["so100","tutorial"]' \
  --control.warmup_time_s=1 \
  --control.episode_time_s=60 \
  --control.reset_time_s=600 \
  --control.num_episodes=2 \
  --control.push_to_hub=false \
  --control.resume=true
# 上传数据
huggingface-cli upload ${hf_user}/${repo_name} path/to/pretrained_model --repo.type=dataset

# 可视化数据
python lerobot/scripts/visualize_dataset_html.py --repo-id weiye11/so100_421_pick --port 9092

# 训练
python lerobot/scripts/train.py \
  --dataset.repo_id=./0605_pi0_100 \
  --policy.type=act \
  --steps=50_000 \
  --save_freq=1_000 \
  --batch_size=8 \
  --output_dir=outputs/0605_pi0_100_act \
  --job_name=0605_pi0_100_act \
  --policy.device=cuda \
  --wandb.enable=true
# 重新训练，需要在pretrained目录下新建亩路，把文件拷贝到路径下


# 部署
python lerobot/scripts/control_robot.py \
  --robot.type=so100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Grasp the colored block, Place it on the black dot, and then return the arm to the default position." \
  --control.repo_id=./eval_pi0_0605_pick_2 \
  --control.tags='["tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=600 \
  --control.reset_time_s=5 \
  --control.num_episodes=10 \
  --control.push_to_hub=false \
  --control.policy.path=/home/kc/workspace/lerobot_pi0_zwy/lerobot/outputs/0613_pi0_Deg2Rad_10w/pretrained_model/


  /home/kc/workspace/lerobot_pi0_zwy/lerobot/outputs/0613_pi0_Deg2Rad_10w/pretrained_model/

  /home/kc/workspace/lerobot_pi0_zwy/lerobot/outputs/0611_pi0_del1c_b32_20w/pretrained_model
  
  /home/kc/workspace/lerobot_pi0_zwy/lerobot/outputs/0611_pi0_del1c_20w/pretrained_model/
  
  /home/kc/workspace/lerobot_pi0_zwy/lerobot/outputs/0609_pi0_del1c/pretrained_model/

  --policy.device=cuda \
  
