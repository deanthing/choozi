export interface IUser {
  name?: string;
  group_id?: number;
  is_owner?: boolean;
  id?: number;
  token?: string;
}

export interface IUserIn {
  name: string;
  group_id: number;
  is_owner: boolean;
  id: number;
  token?: string;
}

interface IStreamingProvider {
  name: string;
  display_priority?: number;
  logo_url?: string;
  tmdb_id?: number;
}
export interface IGenre {
  name: string;
  tmdb_id?: number;
  id?: number;
}

export interface IReleasePeriod {
  lower_bound: number;
  upper_bound: number;
}

export interface IGroup {
  id?: number;
  in_waiting_room?: boolean;
  room_code?: string;
  streaming_providers?: IStreamingProvider[];
  users?: IUserIn[];
  release_period?: IReleasePeriod;
  likes?: ILike[];
  genres?: IGenre[];
  movies?: IMovie[];
}

export interface IMovie {
  id: number;
  tmdb_id: number;
  title: string;
  blurb: string;
  picture_url: string;
  release_date: string;
  streaming_providers: IStreamingProvider[];
  genres: IGenre[];
}

interface ILike {
  group_id: number;
  movie_id: number;
  id: number;
}

export interface IGroupIn {}

export interface IDropDownItem {
  item_id: number;
  name: string;
}

export interface IUserCreateRes {
  token: string;
  user: IUser;
}

export interface ILikeCreate {
  group_id: number;
  movie_id: number;
}
