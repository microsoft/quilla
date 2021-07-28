# Visual Parity

Quilla includes a special `XPath` validation state called `VisualParity`. This page describes what `VisualParity` is in detail, how it can be used for UI regression tests, and how it integrates storage plugins to manage the images it uses and creates. Quilla strives to make the handling of auxiliary data (baseline images, etc) needed by VisualParity as simple as possible.

## What is VisualParity?

VisualParity is a validation state that uses previously accepted screenshots generated by Quilla ("baseline images") to compare against screenshots generated when Quilla is run during testing ("treatment images") to determine if the new screenshots match the old ones. By using VisualParity with sections of a web page, or even the entire page itself, Quilla can give assurances that each section remains the same as it has been from previous runs, allowing users to update only the baseline images related to the work they are doing and protecting the rest of the page from having unexpected visual changes introduced.

## Writing VisualParity Validations

A VisualParity validation is just like any other XPath validation, except that it always requires a Baseline ID to be specified. This baseline ID is assumed to be globally unique- Multiple Quilla test files can refer to the same baseline image by specifying the same ID. An example definition of a VisualParity validation is given below:

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.HomePageContainer }}",
  "state": "VisualParity",
  "parameters": {
    "baselineID": "HomePageContainer"
  }
}
```

### Using Exclusion XPaths

Generally speaking, the higher up in the DOM hierarchy that an element is, the more likely it is that a VisualParity test will be brittle. This can be due to a page that is being changed as part of the regular development cycle, or from having dynamic components (such as time of day/weather/etc.) that will never be consistent between runs. Yet, for most of these tests, what is being tested is not that each individual component (that might have their own VisualParity validation) still looks the same, but that the general layout of the individual components is the same.

To prevent this fragility, Quilla allows test writers to optionally provide a list of exclusion XPaths. These DOM elements that fall below the target XPath will then be censored (i.e. their contents will be covered). This allows VisualParity validations to become more meaningful tests, as individual changes to components that do not alter the visual layout of the page will still allow the validation to pass.

An example definition of a VisualParity validation that specifies exclusion XPaths is given below:

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.HomePageContainer }}",
  "state": "VisualParity",
  "parameters": {
    "baselineID": "HomePageContainer",
    "exclusionXPaths": [
      "${{ Definitions.HomePageHeader }}",
      "${{ Definitions.HomePageFooter }}",
      "${{ Definitions.HomePageDateLabel }}"
    ]
  }
}
```

## Configuring a Storage Plugin

VisualParity requires the ability to store and use images, many of which are required to persist between runs. To do so, it uses one of a few possible "storage plugins"- Quilla Plugins that handle storing, organizing, retrieving, and potentially deleting images. This allows Quilla to simplify the validation logic by outsourcing the image handling at key points to an outside mechanism.

Quilla does not enforce any specific method of configuration for the storage plugins, opting to leave this to plugin authors. To configure an external Quilla storage plugin, please refer to the documentation of that plugin.

Quilla has bundled two storage plugins- a LocalStorage and a BlobStorage plugin. Both of these plugins are configured through CLI that can be reviewed by running `quilla --help`. The LocalStorage plugin requires the specification of a directory in which to store images, and the BlobStorage requires an Azure Blob Storage connection string to connect to a Cloud storage container.

## Creating/Updating Baseline Images

Quilla includes options to create/update baseline images on a per-baseline and a per-file basis. This is done to allow tests to be written that contain multiple `VisualParity` validations while maintaining confidence that updating the baseline image for a specific validation will not create a false positive in any other validation.

To update/create all baseline images for a test file, use the `--update-all-baselines` (or `-U` for shorthand) with the execution. For example, to create all images for a test that uses LocalStorage, run `quilla --image-directory <directory> --update-all-baselines -f <test_file>`.

Alternatively, baseline images can be updated/created individually by specifying their baseline ID. To do so, use the `--update-baseline <BASELINE_ID>` (or `-u <BASELINE_ID>` for shorthand) option, which will execute the Quilla tests normally for all `VisualParity` validations except the ones that have a baseline ID that matches the one specified in the commandline. The `-u/--update-baseline` option can be specified multiple times per run to update multiple baselines during that run. For example, to update the `HomePageHeader` and `HomePageFooter` baselines in LocalStorage, run the command `quilla --image-directory <directory> -u HomePageHeader -u HomePageFooter -f <test_file>`.

## Using VisualParity in CI/CD

Running VisualParity tests in CI/CD platforms allows the automated verification that web page matches the baseline images. This can be particularly helpful as a pre-deployment action to verify that no unexpected frontend changes have occurred before deploying chanegs.

### LocalStorage - Checking In Images

Many cloud CI/CD systems use ephemeral (or effectively ephemeral) runners, which do not save state between runs, or clean up the file system between runs. In these cases, a failed test will give a locator to a file that may no longer exist on the system. However, most CI/CD systems support producing artifacts. Therefore, LocalStorage can be used while still making the run images available by exporting the runs directory as an artifact.

The workflow of using this is as follows:

1. Run `--update-all-baselines` to generate the necessary baseline images and commit them to the repository
1. Run the Quilla tests through the CI system
1. If a test failed, upload the `<image_directory>/runs` folder as an artifact
1. Download the artifact, compare the failed images
1. If baseline images need to be updated, run `--update-baseline <baseline_id>` and commit the new baseline image to the repository

### BlobStorage - Storing Baselines in the Cloud

Azure Blob Storage containers can be used to store both the baseline images as well as treatment images. Using the `--connection-string` CLI option, a connection string can be passed that gives Quilla access to a specific storage account. Optionally, a container name can also be given with the `--container-name` option, but Quilla will by default use a container called "quilla", creating it if it does not exist.

> **Note**: The Azure Blob Storage connection string contains an actual key and **MUST NEVER** be committed to the repository, especially on public repositories. CI systems (such as Github Actions, Azure DevOps, etc.) have secret management systems such as key vaults that are designed to store private information and should be used instead.

The workflow for using Azure Blob Storage with Quilla in CI/CD is as follows:

1. Run `--update-all-baselines` to generate the baselines and upload them to Blob Storage
1. Run Quilla tests through the CI system
1. If a test failed, the test report will include a URL to the treatment and baseline image. Depending on how the storage account is configured, this link might work directly. If the permissions for the storage account do not allow for public view access, the images will need to be downloaded directly from Azure Blob Storage.
1. If baseline images need to be updated, run `--update-baseline <baseline_id>`, which will generate the new baselines and upload them to Blob Storage.

### Limitations / Considerations

Given the distributed/branching model that Git uses, the use of VisualParity tests as part of Pull Request testing should be done through the LocalStorage plugin. This allows particular branches to have different baseline images (since that is provided through Git), which removes potential inconsistencies. For pre- or post-deployment testing, BlobStorage offers a way to store images that is abstracted away from the repository.