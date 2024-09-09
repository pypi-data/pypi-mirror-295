from typing import Literal

GETPaths = Literal[
    "/v1/activity-center",  # This endpoint will retrieve the current activity center entries.
    "/v1/activity-logs",  # This endpoint will retrieve the activity logs. supports precise time filtering with hours and minutes.
    "/v1/agents/get/",  # This endpoint will retrieve a list of all connected agents.
    "/v1/agents/get-all/",  # This endpoint will retrieve a list of all agents.
    "/v1/agents/generate-linking-key/",  # endpoint will generate and retrieve the Agent linking key that will be used during agent installation.
    "/v1/agents/get-hashes/",  # This endpoint will retrieve the hashes for a specific agent
    "/v1/agents/profiles/",  # This endpoint will retrieve a list of profiles for a specific agent, with their username and domain.
    "/v1/apt/attacks",  # This endpoint will retrieve the latest Full Kill-Chain Scenarios report results (overview) by the environment ID.
    "/v1/apt/ids",  # This endpoint will retrieve a list of assessment IDs for the latest run Full Kill-Chain Scenarios assessments.
    "/v1/apt/attack/technical/{id}",  # This endpoint will retrieve Full Kill-Chain Scenarios technical report results for a specific assessment.
    "/v1/apt/history/get-ids/",  # This endpoint will retrieve the Full Kill-Chain Scenarios assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/apt/history/technical/{id}",  # This endpoint will retrieve Full Kill-Chain Scenarios technical report results for a specific assessment
    "/v1/apt/templates/",  # This endpoint will retrieve a list of available Full Kill-Chain Scenarios templates.
    "/v1/apt/template/{id}",  # This endpoint will retrieve a specific Full Kill-Chain Scenarios template by its ID.
    "/v1/apt/status/",  # This endpoint will retrieve a Full Kill-Chain Scenarios assessment status by the assessment ID.
    "/v1/apt/history/technical/detection/{id}",  # This endpoint will retrieve Full Kill-Chain Scenarios detection result data for a specific payload.
    "/v1/apt-wrapper/attacks",  # This endpoint will retrieve the latest Full Kill-Chain Campaign report results (overview) by the environment ID.
    "/v1/apt-wrapper/ids",  # This endpoint will retrieve a list of IDs for the latest Full Kill-Chain Campaign assessments.
    "/v1/apt-wrapper/attack/technical/{id}",  # This endpoint will retrieve Full Kill-Chain Campaign technical report results for a specific assessment.
    "/v1/apt-wrapper/history/get-ids/",  # This endpoint will retrieve the Full Kill-Chain Campaign assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/apt-wrapper/history/technical/{id}",  # This endpoint will retrieve Full Kill-Chain Campaign report results for a specific assessment.
    "/v1/apt-wrapper/templates/",  # This endpoint will retrieve a list of available Full Kill-Chain Campaign templates.
    "/v1/apt-wrapper/status/",  # This endpoint will retrieve a Full Kill-Chain Campaign assessment status by the assessment ID.
    "/v1/browsing/status/",  # This endpoint will retrieve a Web Gateway assessment status by the assessment ID.
    "/v1/browsing/attacks",  # This endpoint will retrieve the latest Web Gateway report results (overview) by the environment ID.
    "/v1/browsing/attacks/technical",  # This endpoint will retrieve the latest Web Gateway technical report results by the environment ID.
    "/v1/browsing/templates/",  # This endpoint will retrieve a list of available Web Gateway templates.
    "/v1/browsing/template/{id}",  # This endpoint will retrieve a specific Web Gateway template by its ID.
    "/v1/browsing/history/get-ids/",  # This endpoint will retrieve the Web Gateway assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/browsing/history/technical/{id}",  # This endpoint will retrieve Web Gateway technical report results for a specific assessment.
    "/v1/browsing/history/executive/{id}",  # This endpoint will retrieve Web Gateway executive report results for a specific assessment.
    "/v1/browsing/feed/url",  # This endpoint will retrieve the list of malicious URLs used in Web Gateway assessments.
    "/v1/dlp/attacks",  # This endpoint will retrieve the latest Data Exfiltration report results (overview) by the environment ID.
    "/v1/dlp/attacks/technical",  # This endpoint will retrieve the latest Data Exfiltration technical report results by the environment ID.
    "/v1/dlp/history/get-ids/",  # This endpoint will retrieve the Data Exfiltration assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/dlp/history/technical/{id}",  # This endpoint will retrieve Data Exfiltration technical report results for a specific assessment.
    "/v1/dlp/history/executive/{id}",  # This endpoint will retrieve Data Exfiltration executive report results for a specific assessment.
    "/v1/dlp/templates/",  # This endpoint will retrieve a list of available Data Exfiltration templates.
    "/v1/dlp/template/{id}",  # This endpoint will retrieve a specific Data Exfiltration template by its ID.
    "/v1/dlp/status/",  # This endpoint will retrieve a Data Exfiltration assessment status by the assessment ID.
    "/v1/edr/attacks",  # This endpoint will retrieve the latest Endpoint Security report results (overview) by the environment ID.
    "/v1/edr/attacks/technical",  # This endpoint will retrieve the latest Endpoint Security technical report results by the environment ID.
    "/v1/edr/attacks/technical/siem",  # This endpoint will retrieve the latest SIEM detection results from Endpoint Security assessments.
    "/v1/edr/history/technical/detection/{id}",  # This endpoint will retrieve detection result data for a specific payload.
    "/v1/edr/attacks/attacknavigator",  # This endpoint will retrieve the latest (overview) Endpoint Security ATT&CK navigator report results by environment ID.
    "/v1/edr/history/attacknavigator/{id}",  # This endpoint will retrieve the Endpoint Security ATT&CK navigator report results for a specific assessment.
    "/v1/edr/history/get-ids/",  # This endpoint will retrieve the Endpoint Security assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/edr/history/technical/{id}",  # This endpoint will retrieve Endpoint Security technical report results for a specific assessment.
    "/v1/edr/history/executive/{id}",  # This endpoint will retrieve Endpoint Security executive report results for a specific assessment.
    "/v1/edr/templates/",  # This endpoint will retrieve a list of available Endpoint Security templates.
    "/v1/edr/template/{id}",  # This endpoint will retrieve a specific Endpoint Security template by its ID.
    "/v1/edr/status/",  # This endpoint will retrieve an Endpoint Security assessment status by the assessment ID.
    "/v1/environments/",  # This endpoint will retrieve a list of all environments, their IDs, agents, and URLs.
    "/v1/all/status/",  # Use this endpoint to get a list of all assessments, their attack IDs, module. and status.
    "/v1/hopper/attacks",  # This endpoint will retrieve the latest Hopper report results (overview) by the environment ID.
    "/v1/hopper/ids",  # This endpoint will retrieve a list of Hopper assessment IDs.
    "/v1/hopper/attack/technical/{id}",  # This endpoint will retrieve Hopper report results for a specific assessment.
    "/v1/hopper/attack/{id}",  # This endpoint will retrieve Hopper technical report results for a specific assessment.
    "/v1/hopper/history/get-ids",  # This endpoint will retrieve the Hopper assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/hopper/history/technical/{id}",  # This endpoint will retrieve Hopper report results for a specific assessment.
    "/v1/hopper/templates/",  # This endpoint will retrieve a list of available Hopper templates.
    "/v1/hopper/status/",  # This endpoint will retrieve a Hopper assessment status by the assessment ID.
    "/v1/immediate-threats/attacks",  # This endpoint will retrieve the latest Immediate Threats report results (overview) by the environment ID.
    "/v1/immediate-threats/ids",  # This endpoint will retrieve a list of IDs for the latest Immediate Threats assessments.
    "/v1/immediate-threats/attack/technical/{id}",  # This endpoint will retrieve Immediate Threats technical report results for a specific assessment.
    "/v1/immediate-threats/history/get-ids/",  # This endpoint will retrieve the Immediate Threats assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/immediate-threats/history/technical/{id}",  # This endpoint will retrieve Immediate Threats report results for a specific assessment.
    "/v1/immediate-threats/list/",  # This endpoint will retrieve a list of Immediate Threats assessments.
    "/v1/immediate-threats/status/",  # This endpoint will retrieve an Immediate Threats assessment status by the assessment ID.
    "/v1/immediate-threats/ioc/",  # This endpoint will retrieve a list of Immediate Threats assessments with their IOCs.
    "/v1/immediate-threats/history/technical/detection/{id}",  # This endpoint will retrieve Immediate Threats detection result data for a specific assessment
    "/v1/integrations/",  # This endpoint will retrieve a list of all connected integrations.
    "/v1/mail/attacks",  # This endpoint will retrieve the latest Email Gateway report results (overview) by the environment ID.
    "/v1/mail/attacks/technical",  # This endpoint will retrieve the latest Email Gateway technical report results by the environment ID.
    "/v1/mail/history/get-ids/",  # This endpoint will retrieve the Email Gateway assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/mail/history/technical/{id}",  # This endpoint will retrieve Email Gateway technical report results for a specific assessment.
    "/v1/mail/history/executive/{id}",  # This endpoint will retrieve Email Gateway executive report results for a specific assessment.
    "/v1/mail/templates",  # This endpoint will retrieve a list of available Email Gateway templates.
    "/v1/mail/template/{id}",  # This endpoint will retrieve a specific Email Gateway template by its ID.
    "/v1/mail/status/",  # This endpoint will retrieve an Email Gateway assessment status by the assessment ID.
    "/v1/phishing/attacks",  # This endpoint will retrieve the latest Phishing Awareness report results (overview) by the environment ID.
    "/v1/phishing/ids",  # This endpoint will retrieve a list of Phishing Awareness assessment IDs.
    "/v1/phishing/attack/technical/{id}",  # This endpoint will retrieve Phishing Awareness report results for a specific assessment.
    "/v1/phishing/history/get-ids/",  # This endpoint will retrieve the Phishing Awareness Campaign assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/phishing/history/technical/{id}",  # This endpoint will retrieve Phishing Awareness Campaign report results for a specific assessment.
    "/v1/phishing/contacts/groups",  # This endpoint will retrieve a list of Phishing Awareness contact groups and their IDs.
    "/v1/phishing/contacts",  # This endpoint will retrieve a list of contacts within a specific contact group by ID.
    "/v1/asm/history/get-ids/",  # This endpoint will retrieve the ASM assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/asm/attack/get-findings",  # This endpoint will retrieve all findings generated in the latest ASM assessment.
    "/v1/asm/attack/get-findings/{ID}",  # This endpoint will retrieve all findings generated in a specific ASM assessment.
    "/v1/asm/attack/get-assets",  # This endpoint will retrieve a list of assets from the latest assessment.
    "/v1/asm/attack/get-assets/{ID}",  # This endpoint will retrieve a list of assets for a specific assessment.
    "/v1/asm/attack/get-outboundips",  # This endpoint will retrieve the list of Outbound IP addresses from the latest assessment.
    "/v1/asm/attack/get-outboundips/{ID}",  # This endpoint will retrieve the list of Outbound IP addresses for a specific assessment.
    "/v1/purple-team/templates/",  # This endpoint will retrieve a list of Advanced Scenarios templates.
    "/v1/purple-team/templates/{id}",  # This endpoint will retrieve a specific Advanced Scenarios template by the template ID.
    "/v1/purple-team/executions/",  # This endpoint will retrieve a list of Advanced Scenarios executions.
    "/v1/purple-team/executions/{id}",  # Get a specific Advanced Scenarios execution.
    "/v1/purple-team/assessments",  # This endpoint will retrieve a list of Advanced Scenarios assessments.
    "/v1/purple-team/assessments/{id}",  # This endpoint will retrieve results for a specific Advanced Scenarios assessment.
    "/v1/purple-team/assessments/findings/{id}",  # This endpoint will retrieve a list of findings for a specific Advanced Scenarios assessment.
    "/v1/purple-team/dashboard",  # This endpoint will retrieve data from the Advanced Scenarios dashboard.
    "/v1/purple-team/check-readiness/{id}",  # This endpoint will retrieve the readiness status for a specific Advanced Scenarios assessment.
    "/v1/user/modules",  # This endpoint will retrieve a list of all available modules in the platform.
    "/v1/user/scores",  # This endpoint will retrieve a list of recent scores for all modules.
    "/v1/user/users",  # This endpoint will retrieve a list of clients and their user information.
    "/v1/user/api-token",  # This endpoint will generate a new API token.
    "/v1/user/api-key",  # This endpoint will return all the API tokens with details.
    "/v1/internal-asm/assessments",  # This endpoint will retrieve Internal ASM assessments.
    "/v1/internal-asm/assessment/{id}",  # This endpoint will retrieve a specific Internal ASM assessment.
    "/v1/waf/attacks",  # This endpoint will retrieve the latest Web Application Firewall report results (overview) by the environment ID.
    "/v1/waf/ids",  # This endpoint will retrieve a list of the latest Web Application Firewall site results and their IDs.
    "/v1/waf/payload-response/{id}",  # This endpoint will retrieve the Web Application Firewall response data for a specific payload.
    "/v1/waf/attack/technical/{SiteID}",  # This endpoint will retrieve the latest technical report results for a specific site.
    "/v1/waf/history/get-ids/",  # This endpoint will retrieve the Web Application Firewall assessment history within the date range provided in the query parameters. If a date range is not provided, the response will retrieve the history from the last 30 days.
    "/v1/waf/history/technical/{id}",  # This endpoint will retrieve Web Application Firewall technical report results for a specific assessment.
    "/v1/waf/history/executive/{id}",  # This endpoint will retrieve Web Application Firewall executive report results for a specific assessment.
    "/v1/waf/site-ids/",  # This endpoint will retrieve a list of site IDs for sites tested in Web Application Firewall assessments.
    "/v1/waf/waf-sites/",  # This endpoint will retrieve a list of sites tested in Web Application Firewall assessments.
    "/v1/waf/templates/",  # This endpoint will retrieve a list of available Web Application Firewall templates.
    "/v1/waf/template/{id}",  # This endpoint will retrieve a specific Web Application Firewall template by its ID.
    "/v1/waf/status/",  # This endpoint will retrieve a Web Application Firewall assessment status by the assessment ID.
    "/msfinding/api/v2/info/{findingID}",  # This endpoint retrieves and returns more detailed information about a specific finding, identified by its finding ID. You can get finding IDs using the /msfinding/api/v2/search endpoint.
    "/msfinding/api/v2/mitre-dashboard-to-json",  # Get the Mitre ATT&CK layer navigator from the Heatmap dashboard.
]

POSTPaths = Literal[
    "/v1/agents/agent-token/",  # This endpoint will retrieve an agent token and token expiration date.
    "/v1/agents/uninstall/{id}",  # This endpoint will uninstall a specific agent by the agent ID.
    "/v1/agents/update/",  # This endpoint will update a specific agent to the latest version
    "/v1/agents/profile/",  # This endpoint will create a new profile for a specific agent (relevant for Service-based agents only).  This action may take a few seconds.
    "/v1/apt/start/",  # This endpoint will launch a Full Kill-Chain Scenarios assessment based on the values provided in the request body.
    "/v1/apt/stop/",  # This endpoint will stop a Full Kill-Chain Scenarios assessment that is running.
    "/v1/apt-wrapper/start/",  # This endpoint will launch a Full Kill-Chain Campaign assessment based on the values provided in the request body.
    "/v1/apt-wrapper/stop/",  # This endpoint will stop a Full Kill-Chain Campaign assessment that is running.
    "/v1/browsing/start/",  # This endpoint will launch a Web Gateway assessment based on the values provided in the request body.
    "/v1/browsing/stop/",  # This endpoint will stop a Web Gateway assessment that is running.
    "/v1/browsing/upload-urls",  # This endpoint will allow uploading URL resources based on the values provided in the request body
    "/v1/dlp/start/",  # This endpoint will launch a Data Exfiltration assessment based on the values provided in the request body.
    "/v1/dlp/stop/",  # This endpoint will stop a Data Exfiltration assessment that is running.
    "/v1/edr/start/",  # This endpoint will launch an Endpoint Security assessment based on the values provided in the request body.
    "/v1/edr/stop/",  # This endpoint will stop an Endpoint Security assessment that is running.
    "/v1/hopper/start/",  # This endpoint will launch a Hopper assessment based on the values provided in the request body.
    "/v1/hopper/stop/",  # This endpoint will stop a Hopper assessment that is running.
    "/v1/immediate-threats/start/",  # This endpoint will launch an Immediate Threats assessment based on the values provided in the request body.
    "/v1/immediate-threats/stop/",  # This endpoint will stop an Immediate Threats assessment that is running.
    "/v1/immediate-threats/upload/",  # This endpoint will create a new Immediate Threat simulation according to the values described in the request body.
    "/v1/mail/start/",  # This endpoint will launch an Email Gateway assessment based on the values provided in the request body.
    "/v1/mail/stop/",  # This endpoint will stop an Email Gateway assessment that is running.
    "/v1/mail/upload-urls/",  # This endpoint will add new URL resources based on the values provided in the request body.
    "/v1/phishing/contacts/group",  # This endpoint can be used to create a contact group under Phishing Awareness > Contacts.
    "/v1/phishing/contacts/upload",  # Use this endpoint to upload a .csv file with contacts to add to a specific group. The .csv file should have each contact in a separate line (First name and last name are optional). The.csv file should be saved in a UTF8 format.
    "/v1/purple-team/templates/",  # This endpoint will create a new Advanced Scenarios template based on the values provided in the request body.
    "/v1/purple-team/executions/",  # This endpoint will create a new Advanced Scenarios execution based on the values provided in the request body.
    "/v1/purple-team/file/",  # This endpoint will create a new Advanced Scenarios file based on the values provided in the request body.
    "/v1/purple-team/assessment",  # This endpoint will create a new Advanced Scenarios assessment based on the values provided in the request body.
    "/v1/purple-team/assessment/launch/{id}",  # This endpoint will launch an Advanced Scenarios assessment by the assessment ID.
    "/v1/purple-team/check-readiness/{id}",  # This endpoint will check readiness for a specific Advanced Scenarios assessment.
    "/v1/user/{clientId}",  # Creates a new user account with details such as name, email, and role. The request body should include first name, last name, email, and role ID.
    "/v1/user/reset-2fa/{id}",  # Reset a user 2FA.
    "/v1/user/resend-invitation/{id}",  # Resend invitation for a user.
    "/v1/user/edit-environment/{id}",  # Add agents/email addresses to an environment using the environment ID and an array of agents/email addresses that you want to add.<br/> <strong>Note:</strong> This action will override the agent/email address list in the destination environment.<br/> <strong>Note:</strong> To remove all agents/email addresses from an environment, enter the environment ID parameter and an empty array in the request body.
    "/v1/internal-asm/launchAssessment",  # This endpoint will create an Internal ASM assessment.
    "/v1/waf/start/",  # This endpoint will launch a Web Application Firewall assessment based on the values provided in the request body.
    "/v1/waf/stop/",  # This endpoint will stop a Web Application Firewall assessment that is running.
    "/v1/waf/waf-site/",  # Used to add Web Application Firewall sites to be used to launch assessments.
    "/msfinding/api/v2/filters",  # This endpoint will retrieve finding filter options from the Findings page.
    "/msfinding/api/v2/search",  # This endpoint will retrieve findings from the Findings page. Define the filters in the request body to refine the results.
    "/msfinding/api/v2/tags",  # This endpoint will add tags to findings. Enter the tags and the finding ID in the request body to attach the tags to those findings. You can get finding IDs using the /msfinding/api/v2/search endpoint.
]

PUTPaths = Literal[
    "/v1/agents/change-environment/",  # This endpoint will move an agent to a specific environment.
    "/v1/agents/profile/",  # This endpoint will reset the password for a profile. This action may take a few seconds.
    "/v1/purple-team/templates/{id}",  # This endpoint will edit an existing Advanced Scenarios template based on the values provided in the request body.
    "/v1/user/{id}",  # Updates user Role for the specified user ID.
    "/v1/user/permissions/{id}",  # Updates permissions for a given user. The request body should specify the updated permissions.
    "/v1/user/email-preferences/{id}",  # Updates email preferences for a specific user. The request body should include the updated email preferences settings.
    "/v1/internal-asm/updateAssessment",  # Update an Internal ASM assessment
]

DELETEPaths = Literal[
    "/v1/agents/profile/",  # This endpoint will delete a profile from an agent.
    "/v1/agents/{id}",  # This endpoint will delete a specific agent by the agent ID.
    "/v1/phishing/contacts",  # Use this endpoint to upload a list of comma-separated email addresses to be removed from the contacts database in phishing, the contacts will be removed from all groups they belong to.
    "/v1/purple-team/templates/{id}",  # This endpoint will delete a specific Advanced Scenarios template by the template ID.
    "/v1/purple-team/executions",  # This endpoint will delete a specific user-created Advanced Scenarios executions by the execution ID. Cymulate executions cannot be deleted.
    "/v1/purple-team/execution/{id}",  # This endpoint will delete a specific user-created Advanced Scenarios execution by the execution ID. Cymulate executions cannot be deleted.
    "/v1/purple-team/assessment/{id}",  # This endpoint will delete a specific Advanced Scenarios assessment by the assessment ID.
    "/v1/user/{id}",  # Deletes a user with the specified user ID. Returns an error if attempting to delete the last user in the account.
    "/v1/internal-asm/assessment/{id}",  # This endpoint will delete a specific Internal ASM assessment.
]
