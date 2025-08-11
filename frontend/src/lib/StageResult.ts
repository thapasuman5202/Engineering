export interface StageResult<T = unknown> {
  stage: number
  status: string
  data?: T
}
