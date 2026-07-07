from datetime import datetime
from nomba.careTakerServices.app.repository.maintenance_request_repo import MaintenanceRequestRepo


class MaintenanceRequestService:
    def __init__(self, repo: MaintenanceRequestRepo):
        self.repo = repo

    async def create_request(self, title: str, priority: str, unit: str, property_name: str, care_taker_id: str):
        data = {
            "title": title,
            "priority": priority,
            "unit": unit,
            "property_name": property_name,
            "care_taker_id": care_taker_id,
            "status": "Open",
            "reported_date": datetime.now().strftime("%Y-%m-%d"),
        }
        return await self.repo.create_request(data)

    async def get_all_requests(self):
        return await self.repo.get_all_requests()

    async def update_status(self, request_id: str, status: str) -> bool:
        return await self.repo.update_status(request_id, status)

    async def get_task_summary(self):
        open_count = await self.repo.count_by_status("Open")
        in_progress_count = await self.repo.count_by_status("In Progress")
        completed_count = await self.repo.count_by_status("Completed")
        return {
            "open": open_count,
            "in_progress": in_progress_count,
            "completed": completed_count,
        }
