# CDS QMIX & QPLEX for Google Research Football MARL
This repo provides our modification of the original CDS implementation for our GRF MARL Benchmark, including new environment settings, feature encoders and reward functions, etc.

## Experiment
To run the experiments:

```sh
cd CDS_GRF
run either tmux_run_qmix.sh or tmux_run_qplex.sh. (You probably need to install tmux first to run all tasks parallely.)
```

The detailed configurations of each environment is in `/CDS_GRF/config`.

## Contact
Feel free to leave an issue if you have any questions about this repo. You can also contact current maintainers, [YanSong97](https://github.com/YanSong97) and [DiligentPanda](https://github.com/DiligentPanda), by email.

# CDS: Celebrating Diversity in Shared Multi-Agent Reinforcement Learning

The paper is now available in [arXiv](https://arxiv.org/pdf/2106.02195.pdf) and accepted by NeurIPS 2021. Our approach can help both value-based and policy-based baselines (such as QMIX, QPLEX, and MAPPO) to explore sophisticated strategies for improving learning efficiency in challenging benchmarks.

## Note

This codebase accompanies the paper submission "Celebrating Diversity in Shared Multi-Agent Reinforcement Learning"([CDS website](https://sites.google.com/view/celebrate-diversity-shared)) and is based on [GRF](https://github.com/google-research/football), [PyMARL](https://github.com/oxwhirl/pymarl) and [SMAC](https://github.com/oxwhirl/smac) codebases which are open-sourced.

## Publication

If you find this repository useful, please cite our paper:
```
@article{chenghao2021celebrating,
  title={Celebrating diversity in shared multi-agent reinforcement learning},
  author={Li, Chenghao, and Wang, Tonghan and Wu, Chengjie and Zhao, Qianchuan and Yang, Jun and Zhang, Chongjie},
  journal={Advances in Neural Information Processing Systems},
  volume={34},
  year={2021}
}
```
