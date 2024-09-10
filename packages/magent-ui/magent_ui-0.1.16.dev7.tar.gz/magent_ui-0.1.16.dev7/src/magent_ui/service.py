from agentuniverse_product.service.agent_service.agent_service import AgentService
from agentuniverse_product.service.workflow_service.workflow_service import WorkflowService
from agentuniverse_product.service.knowledge_service.knowledge_service import KnowledgeService
from agentuniverse_product.service.llm_service.llm_service import LLMService
from agentuniverse_product.base.util.common_util import is_component_id_unique
from agentuniverse_product.service.plugin_service.plugin_service import PluginService
from agentuniverse_product.service.session_service.session_service import SessionService
from agentuniverse_product.service.tool_service.tool_service import ToolService


class AUService():
    agentService = AgentService
    workflowService = WorkflowService
    knowledgeService = KnowledgeService
    llmService = LLMService
    pluginService = PluginService
    sessionService = SessionService
    toolService = ToolService
    is_component_id_unique = is_component_id_unique


au_service = AUService()
