# KubeDigestUpdater
Welcome to KubeDigestUpdater, a Python project focused on observing image freshness and redeploying pods when their digests are no longer up to date!

## About
KubeDigestUpdater is a personal project aimed at expanding my Python proficiency while addressing a specific need in Kubernetes management. As Python isn't my primary language (Java is), this project serves as a practical way to gain hands-on experience with Python programming and its ecosystem.
However, KubeDigestUpdater is primarily about learning and giving back to the open-source community.

## Features
 - Automatic Image Observation: Automatically monitors image freshness to ensure pods are redeployed when their digests become outdated.
 - Kubernetes Integration: Seamlessly integrates with Kubernetes to manage image digests within your cluster.
 - Simplified Pod Management: Streamlines pod redeployment processes by handling image updates efficiently.

## Usage
 - Annotate your StatefulSets, Deployments, or DaemonSets with a specific annotation to trigger the automatic image digest monitoring. Simply add the annotation to the metadata of your desired resources.
 - Ensure that your container's pullPolicy is set to "Always" to maintain consistency, as the tag remains the same.
 - KubeDigestUpdater will automatically handle the rest! It periodically (adjustable interval) checks the image digest of the deployed pod or container against the latest digest of the same image in the registry. If the registry digest differs, the pod is automatically redeployed.

## Limitations
KubeDigestUpdater does not handle Git commits or version increments. Its focus is solely on managing image digests for containers with consistent tags e.g. latest on development or stage environments.

## Status
KubeDigestUpdater is currently under development. Helm charts are available and will be refined further before being provided for use.

## Contributions
Contributions to KubeDigestUpdater are welcome once a certain level of functionality is achieved! If you spot bugs, have feature ideas, or want to improve the code, feel free to open issues or pull requests. Let's learn and grow together!

## License
This project is licensed under the Apache 2.0 License. You are encouraged to use, modify, and distribute the code. See the LICENSE file for more details.