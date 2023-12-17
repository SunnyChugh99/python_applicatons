#!/bin/bash
set -x # Activate debugging to show execution details: all commands will be printed before execution

echo "User creation..."

if [[ $USER_IMPERSONATION == "true" ]]; then
    echo "[INFO]: user impersonation is True"
    sudo groupadd -g $group_id_1 $group_name_1
    sudo useradd -mu $user_id -g $group_name_1 $user_name
    sudo usermod -aG sudo $user_name
    sudo chmod -R 777 /home/$user_name
    sudo su -c 'echo "PATH='"$PATH"'" > /etc/environment' root
    sudo su -c 'echo "'"$user_name"' ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers' root
    sudo su -c 'echo %"'"$user_name"' ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers' root
    sudo chown -R $user_name:$group_name_1 /config
    sudo chown -R $user_name:$group_name_1 /notebooks
    sudo chown -R $user_name:$group_name_1 /etc/nginx
    sudo echo "umask $NB_UMASK" >> ~/.bashrc; echo "umask $NB_UMASK" >> /etc/profile; echo "umask $NB_UMASK" >> /etc/profile.d/umask.sh; echo "umask $NB_UMASK" >> /home/$user_name/.bashrc;
    sudo su -c 'sudo echo "umask '"$NB_UMASK"'" >> ~/.shrc'

    if [[ ${number_of_groups} -gt 1 ]]; then
        for ((n=2;n<=${number_of_groups};n++))
        do
          group_id_var="\${group_id_${n}}"
          group_name_var="\${group_name_${n}}"
          eval group_id="$group_id_var"
          eval group_name="$group_name_var"
          sudo groupadd --gid ${group_id} ${group_name}
          sudo usermod -a -G ${group_name} ${user_name}
        done
    fi
else
    user_name="mosaic-ai"
fi
